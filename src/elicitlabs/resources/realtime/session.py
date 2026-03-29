from __future__ import annotations

import re
import json
import struct
import asyncio
from typing import Any, List, Optional, AsyncIterator

from ..._exceptions import ElicitClientError
from ...types.realtime.session_events import (
    ErrorEvent,
    ContextCard,
    StatusEvent,
    WorkingMemory,
    LongTermMemory,
    ShortTermMemory,
    TranscriptEvent,
    StmTranscriptTurn,
    SessionEndedEvent,
    SessionInitEvent,
    SessionReadyEvent,
    MemoryUpdateEvent,
    ContextStatusEvent,
    ContextUpdateEvent,
    ContextSnapshotEvent,
    SnapshotWorkingMemory,
    SnapshotShortTermMemory,
    RealtimeSessionEvent,
)

try:
    import websockets
    from websockets.asyncio.client import ClientConnection
except ImportError:
    websockets = None  # type: ignore[assignment]
    ClientConnection = None  # type: ignore[misc,assignment]


__all__ = [
    "AsyncRealtimeSession",
    "ContextAccumulator",
]

GATEWAY_URL_DEFAULT = "wss://gateway.elicitlabs.ai/ws"

FRAME_AUDIO: int = 0x01
FRAME_VIDEO: int = 0x02

VIDEO_SUB_JPEG: int = 0x00
VIDEO_SUB_RAW: int = 0x01

SAMPLE_RATE: int = 16_000
CHANNELS: int = 1
BYTES_PER_SAMPLE: int = 2
CHUNK_DURATION_MS: int = 20
SAMPLES_PER_CHUNK: int = SAMPLE_RATE * CHUNK_DURATION_MS // 1000
BYTES_PER_CHUNK: int = SAMPLES_PER_CHUNK * CHANNELS * BYTES_PER_SAMPLE

_EVENT_TYPE_MAP: dict[str, type[Any]] = {
    "session_ready": SessionReadyEvent,
    "session_init": SessionInitEvent,
    "memory_update": MemoryUpdateEvent,
    "transcript": TranscriptEvent,
    "context_update": ContextUpdateEvent,
    "context_snapshot": ContextSnapshotEvent,
    "context_status": ContextStatusEvent,
    "session_ended": SessionEndedEvent,
    "error": ErrorEvent,
    "status": StatusEvent,
}


def _parse_event(raw: dict[str, Any]) -> Optional[RealtimeSessionEvent]:
    """Parse a raw JSON dict into a typed event, or ``None`` for unknown types."""
    event_type = raw.get("type", "")
    normalized = event_type.lower()
    cls = _EVENT_TYPE_MAP.get(normalized)
    if cls is None:
        return None
    # Normalize the type field to lowercase so Literal validators match
    if event_type != normalized:
        raw = {**raw, "type": normalized}
    return cls.model_validate(raw)  # type: ignore[return-value]


class ContextAccumulator:
    """Collects realtime events and builds unified context for LLM injection.

    Supports both the new ``CONTEXT_SNAPSHOT`` events (full-state replacement)
    and legacy ``CONTEXT_UPDATE`` / ``MEMORY_UPDATE`` events (delta-based).

    For legacy events, maintains a **card store** keyed by ``card.id`` with
    ``add``, ``update``, and ``expire`` operations.

    For ``CONTEXT_SNAPSHOT`` events, replaces all state atomically and also
    populates the legacy card store for backward compatibility.
    """

    # Card types grouped by output section (legacy)
    SCENE_FACT_TYPES = frozenset({"face_identity", "speaker_identity", "scene_fact", "attention_target"})
    SYSTEM_PROMPT_TYPES = frozenset({"identity", "preference"})
    EPISODE_TYPES = frozenset({"episodic"})

    def __init__(self) -> None:
        self.card_store: dict[str, ContextCard] = {}
        """Card store keyed by card.id. Apply ops to maintain."""

        self._flushed_system_prompt: set[str] = set()
        self.messages: List[Any] = []
        self.transcripts: List[str] = []
        self._context_version = 0

        self.working_memory: Optional[WorkingMemory] = None
        """Latest legacy working memory (from MEMORY_UPDATE or CONTEXT_UPDATE)."""

        self.short_term_memory: Optional[Any] = None
        """Latest legacy short-term memory from MEMORY_UPDATE."""

        self.active_entities: dict[str, dict[str, str]] = {}
        """Entity presence map from the latest CONTEXT_STATUS heartbeat.
        Keyed by entity_id -> {name, modality}."""

        self.stm_prior_transcripts: List[Any] = []
        """Prior transcript segments from SESSION_INIT (cross-session context)."""

        self.stm_prior_entities: List[Any] = []
        """Prior entity observations from SESSION_INIT (cross-session context)."""

        # --- CONTEXT_SNAPSHOT state (new) ---

        self.turn_id: Optional[int] = None
        """Latest turn_id from any event."""

        self.ts: Optional[float] = None
        """Timestamp of the latest snapshot."""

        self.snapshot_working_memory: Optional[SnapshotWorkingMemory] = None
        """Latest working memory from CONTEXT_SNAPSHOT (speakers, objects, summary, topics, people)."""

        self.snapshot_short_term_memory: Optional[SnapshotShortTermMemory] = None
        """Latest short-term memory from CONTEXT_SNAPSHOT (messages list)."""

        self.long_term_memory: Optional[LongTermMemory] = None
        """Latest long-term memory from CONTEXT_SNAPSHOT (episodic, preference, identity)."""

    @property
    def cards(self) -> List[ContextCard]:
        """All cards currently in the store (convenience accessor)."""
        return list(self.card_store.values())

    def reset(self) -> None:
        """Clear all accumulated state (preserves flushed system_prompt tracker)."""
        self.card_store.clear()
        self.messages.clear()
        self.transcripts.clear()
        self._context_version = 0
        self.working_memory = None
        self.short_term_memory = None
        self.turn_id = None
        self.ts = None
        self.snapshot_working_memory = None
        self.snapshot_short_term_memory = None
        self.long_term_memory = None

    @staticmethod
    def _dedup_key(card: ContextCard) -> str:
        """Normalize a claim for dedup: strip confidence %, scores, and
        collapse whitespace so the same entity/fact isn't stored twice."""
        claim = card.claim or ""
        claim = re.sub(r"\(.*?confidence.*?\)", "", claim)
        claim = re.sub(r"\d+%", "", claim)
        claim = re.sub(r"\s+", " ", claim).strip()
        return f"{card.type}:{claim}"

    def on_session_init(self, event: SessionInitEvent) -> None:
        """Process a SESSION_INIT event: store prior cross-session context from STM."""
        if event.stm_prior_transcripts:
            self.stm_prior_transcripts = list(event.stm_prior_transcripts)
        if event.stm_prior_entities:
            self.stm_prior_entities = list(event.stm_prior_entities)
            # Seed active_entities from prior session data
            for ent in event.stm_prior_entities:
                if ent.entity_id and ent.entity_name:
                    self.active_entities[ent.entity_id] = {
                        "name": ent.entity_name,
                        "modality": ent.modality or "unknown",
                    }

    def on_memory_update(self, event: MemoryUpdateEvent) -> None:
        """Process a MEMORY_UPDATE event: update STM transcript and working memory."""
        if event.turn_id is not None:
            self.turn_id = event.turn_id
        if event.short_term_memory is not None:
            self.short_term_memory = event.short_term_memory
        if event.working_memory is not None:
            self.working_memory = event.working_memory

    def on_context_update(self, event: ContextUpdateEvent) -> None:
        """Process a CONTEXT_UPDATE event: apply card ops, update working memory."""
        if event.turn_id is not None:
            self.turn_id = event.turn_id
        version = event.context_version or 0
        self._context_version = max(self._context_version, version)

        for op in event.ops or []:
            if op.op == "add" and op.card is not None:
                card_id = op.card.id
                if card_id:
                    self.card_store[card_id] = op.card
                else:
                    # Fallback for cards without an id — use dedup key
                    fallback_id = self._dedup_key(op.card)
                    self.card_store[fallback_id] = op.card

            elif op.op == "update" and op.card_id:
                existing = self.card_store.get(op.card_id)
                if existing is not None and op.updates:
                    # Merge updates into existing card
                    data = existing.model_dump()
                    data.update(op.updates)
                    self.card_store[op.card_id] = ContextCard.model_validate(data)

            elif op.op == "expire" and op.card_id:
                self.card_store.pop(op.card_id, None)

            # Legacy support: 'remove' treated as 'expire'
            elif op.op == "remove" and op.card_id:
                self.card_store.pop(op.card_id, None)

        for msg in event.messages or []:
            self.messages.append(msg)

        if event.working_memory is not None:
            self.working_memory = event.working_memory

    def on_context_status(self, event: ContextStatusEvent) -> None:
        """Process a CONTEXT_STATUS heartbeat: update entity presence and working memory."""
        version = event.context_version or 0
        self._context_version = max(self._context_version, version)

        if event.active_entities is not None:
            self.active_entities = dict(event.active_entities)

        if event.working_memory is not None:
            self.working_memory = event.working_memory

    def on_transcript(self, event: TranscriptEvent) -> None:
        text = event.text or ""
        if text.strip():
            self.transcripts.append(text)

    def on_context_snapshot(self, event: ContextSnapshotEvent) -> None:
        """Process a CONTEXT_SNAPSHOT event: replace full state.

        Unlike ``CONTEXT_UPDATE`` (which applies deltas via card ops),
        ``CONTEXT_SNAPSHOT`` delivers the complete current state.  The SDK
        replaces all previous state on each snapshot.

        Also populates legacy fields (``working_memory``, ``short_term_memory``,
        ``card_store``) for backward compatibility.
        """
        if event.turn_id is not None:
            self.turn_id = event.turn_id
        if event.ts is not None:
            self.ts = event.ts

        # Full replacement — not merge
        if event.working_memory is not None:
            self.snapshot_working_memory = event.working_memory
            # Populate legacy working_memory for backward compat
            self.working_memory = WorkingMemory(
                conversation_summary=event.working_memory.conversation_summary,
                topic_summaries=event.working_memory.topics,
                people=event.working_memory.people,
                scene=None,
            )

        if event.short_term_memory is not None:
            self.snapshot_short_term_memory = event.short_term_memory
            # Populate legacy short_term_memory for backward compat
            if event.short_term_memory.messages:
                turns = []
                for msg in event.short_term_memory.messages:
                    turns.append(StmTranscriptTurn(
                        role=msg.role,
                        speaker=msg.speaker,
                        content=msg.content,
                        ts=msg.ts,
                    ))
                self.short_term_memory = ShortTermMemory(transcript=turns)

        if event.long_term_memory is not None:
            self.long_term_memory = event.long_term_memory
            self._sync_ltm_to_cards(event.long_term_memory)

    def _sync_ltm_to_cards(self, ltm: LongTermMemory) -> None:
        """Sync LongTermMemory string arrays into the card_store for backward compat.

        Since snapshots are full-state, clears existing cards of LTM types
        and replaces with the new data.
        """
        ltm_types = {"episodic", "preference", "identity"}
        to_remove = [k for k, v in self.card_store.items() if v.type in ltm_types]
        for k in to_remove:
            del self.card_store[k]

        for card_type, claims in [
            ("episodic", ltm.episodic or []),
            ("preference", ltm.preference or []),
            ("identity", ltm.identity or []),
        ]:
            for i, claim in enumerate(claims):
                card_id = f"ltm_{card_type}_{i}"
                self.card_store[card_id] = ContextCard(
                    id=card_id,
                    type=card_type,
                    claim=claim,
                )

    def build_llm_prompt(self) -> str:
        """Build an LLM-ready prompt from the latest CONTEXT_SNAPSHOT data.

        Returns a structured string with sections for people present, objects
        in scene, conversation summary, long-term memories, and conversation
        history.  Falls back to :meth:`build_context_string` if no snapshot
        data is available.

        The output follows the format from the CONTEXT_SNAPSHOT migration guide
        and can be used directly as a system message.
        """
        wm = self.snapshot_working_memory
        stm = self.snapshot_short_term_memory
        ltm = self.long_term_memory

        # Fall back to legacy format if no snapshot data
        if wm is None and stm is None and ltm is None:
            return self.build_context_string()

        system_parts: list[str] = []

        if wm is not None:
            if wm.speakers:
                system_parts.append("## People Present")
                for s in wm.speakers:
                    system_parts.append(f"- {s.description or s.name or '?'}")

            if wm.objects:
                system_parts.append("\n## Objects in Scene")
                for o in wm.objects:
                    system_parts.append(f"- {o.description or o.label or '?'}")

            if wm.conversation_summary:
                system_parts.append(f"\n## Conversation Summary\n{wm.conversation_summary}")

        if ltm is not None:
            has_memories = (ltm.episodic or ltm.preference or ltm.identity)
            if has_memories:
                system_parts.append("\n## Memories")
                for mem in (ltm.episodic or []):
                    system_parts.append(f"- [Episode] {mem}")
                for mem in (ltm.preference or []):
                    system_parts.append(f"- [Preference] {mem}")
                for mem in (ltm.identity or []):
                    system_parts.append(f"- [Identity] {mem}")

        messages: list[dict[str, str]] = []
        if system_parts:
            messages.append({"role": "system", "content": "\n".join(system_parts)})

        if stm is not None and stm.messages:
            for msg in stm.messages:
                role = msg.role or "user"
                speaker = msg.speaker or ""
                content = msg.content or ""
                if role == "user":
                    messages.append({"role": "user", "content": f"{speaker}: {content}" if speaker else content})
                else:
                    messages.append({"role": "assistant", "content": content})

        if not messages:
            return "(no context available)"

        # Render as a single string with role labels
        parts: list[str] = []
        for msg in messages:
            parts.append(f"[{msg['role']}]\n{msg['content']}")
        return "\n\n".join(parts)

    def build_llm_messages(
        self,
        user_question: str = "Respond based on the context above.",
    ) -> list[dict[str, str]]:
        """Return a ``messages`` list suitable for ``openai.chat.completions.create()``
        or ``anthropic.messages.create()``.

        If CONTEXT_SNAPSHOT data is available, uses the snapshot format.
        Otherwise falls back to the legacy context string.
        """
        wm = self.snapshot_working_memory
        stm = self.snapshot_short_term_memory
        ltm = self.long_term_memory

        if wm is not None or stm is not None or ltm is not None:
            # Build from snapshot data
            system_parts: list[str] = []

            if wm is not None:
                if wm.speakers:
                    system_parts.append("## People Present")
                    for s in wm.speakers:
                        system_parts.append(f"- {s.description or s.name or '?'}")

                if wm.objects:
                    system_parts.append("\n## Objects in Scene")
                    for o in wm.objects:
                        system_parts.append(f"- {o.description or o.label or '?'}")

                if wm.conversation_summary:
                    system_parts.append(f"\n## Conversation Summary\n{wm.conversation_summary}")

            if ltm is not None:
                has_memories = (ltm.episodic or ltm.preference or ltm.identity)
                if has_memories:
                    system_parts.append("\n## Memories")
                    for mem in (ltm.episodic or []):
                        system_parts.append(f"- [Episode] {mem}")
                    for mem in (ltm.preference or []):
                        system_parts.append(f"- [Preference] {mem}")
                    for mem in (ltm.identity or []):
                        system_parts.append(f"- [Identity] {mem}")

            messages: list[dict[str, str]] = [
                {"role": "system", "content": "\n".join(system_parts) if system_parts else ""},
            ]

            if stm is not None and stm.messages:
                for msg in stm.messages:
                    role = msg.role or "user"
                    speaker = msg.speaker or ""
                    content = msg.content or ""
                    if role == "user":
                        messages.append({"role": "user", "content": f"{speaker}: {content}" if speaker else content})
                    else:
                        messages.append({"role": "assistant", "content": content})

            messages.append({"role": "user", "content": user_question})
            return messages

        # Legacy fallback
        context = self.build_context_string()
        return [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Use the following retrieved "
                    "context to inform your response.\n\n" + context
                ),
            },
            {"role": "user", "content": user_question},
        ]

    def build_context_dict(self) -> dict[str, str]:
        """Return context as a dict with five keys:

        * ``scene_facts`` — face/speaker identity, scene facts, attention targets
        * ``system_prompt`` — **only new** identity/preference claims not yet flushed
        * ``episodes`` — episodic memories
        * ``transcript`` — accumulated transcript text
        * ``working_memory`` — pre-rendered working memory summary from the server

        Each value is a plain string (empty string if nothing in that section).
        Identity/preference claims are tracked across flushes so they are
        only returned once.
        """
        all_cards = self.cards
        scene_facts = [c for c in all_cards if c.type in self.SCENE_FACT_TYPES]
        all_system = [c for c in all_cards if c.type in self.SYSTEM_PROMPT_TYPES]
        episodes = [c for c in all_cards if c.type in self.EPISODE_TYPES]

        # Only include system_prompt entries that haven't been flushed before
        new_system: list[ContextCard] = []
        for c in all_system:
            key = self._dedup_key(c)
            if key not in self._flushed_system_prompt:
                new_system.append(c)
                self._flushed_system_prompt.add(key)

        # Build working memory text from structured fields
        wm_parts: list[str] = []
        if self.working_memory:
            wm = self.working_memory
            if wm.conversation_summary:
                wm_parts.append(f"Summary: {wm.conversation_summary}")
            if wm.topic_summaries:
                wm_parts.append(f"Topics: {', '.join(wm.topic_summaries)}")
            if wm.people:
                for p in wm.people:
                    wm_parts.append(f"[{p.role or '?'}] {p.name or '?'}: {p.context or ''}")
            if wm.scene:
                for s in wm.scene:
                    wm_parts.append(f"[scene] {s.content or '?'} (salience={s.salience or 0:.2f})")

        return {
            "scene_facts": "\n".join(f"[{c.type}] {c.claim or ''}" for c in scene_facts),
            "system_prompt": "\n".join(c.claim or "" for c in new_system),
            "episodes": "\n".join(c.claim or "" for c in episodes),
            "transcript": " ".join(self.transcripts),
            "working_memory": "\n".join(wm_parts),
        }

    def build_context_string(self) -> str:
        """Build a single context string from all sections."""
        ctx = self.build_context_dict()
        sections: list[str] = []
        for key in ("working_memory", "scene_facts", "system_prompt", "episodes", "transcript"):
            if ctx[key]:
                sections.append(f"{key}:\n{ctx[key]}")
        return "\n\n".join(sections) if sections else "(no context retrieved)"


class AsyncRealtimeSession:
    """An active WebSocket session with the Elicit Labs realtime gateway.

    This object is both an async context manager and an async iterator::

        async with session:
            await session.send_audio(pcm_bytes)
            async for event in session:
                ...

    Attributes:
        context: A :class:`ContextAccumulator` that is automatically fed
            every ``context_update`` and ``transcript`` event.
        session_id: The server-assigned session ID (set after the handshake).

    """

    context: ContextAccumulator
    session_id: Optional[str]

    def __init__(
        self,
        *,
        api_key: str,
        user_id: str,
        session_id: str,
        generation: bool = True,
        gateway_url: Optional[str] = None,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        disabled_learning: bool = False,
        auto_listen: bool = True,
    ) -> None:
        if websockets is None:
            raise ElicitClientError(
                "The 'websockets' package is required for realtime sessions. "
                "Install it with:  pip install 'elicitlabs[realtime]'"
            )

        self._api_key = api_key
        self._user_id = user_id
        self._init_session_id = session_id
        self._generation = generation
        self._gateway_url = gateway_url or GATEWAY_URL_DEFAULT
        self._project_id = project_id
        self._persona_id = persona_id
        self._disabled_learning = disabled_learning
        self._auto_listen = auto_listen

        self.context = ContextAccumulator()
        self.session_id = None
        self.status: str = "rest"
        """Pipeline status: ``"rest"`` (idle/done) or ``"processing"``."""
        self._ws: Optional[ClientConnection] = None
        self._closed = False
        self._iter_done = False
        self._listener_task: Optional[asyncio.Task[None]] = None

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    async def _connect(self) -> None:
        assert websockets is not None

        try:
            self._ws = await websockets.connect(  # type: ignore[union-attr]
                self._gateway_url,
                max_size=10 * 1024 * 1024,
            )
        except Exception as exc:
            raise ElicitClientError(
                f"Could not connect to gateway at {self._gateway_url}: {exc}"
            ) from exc

        init_msg: dict[str, Any] = {
            "token": self._api_key,
            "session_id": self._init_session_id,
            "user_id": self._user_id,
            "generation": self._generation,
            "disabled_learning": self._disabled_learning,
        }
        if self._project_id is not None:
            init_msg["project_id"] = self._project_id
        if self._persona_id is not None:
            init_msg["persona_id"] = self._persona_id

        await self._ws.send(json.dumps(init_msg))

        try:
            resp_raw = await asyncio.wait_for(self._ws.recv(), timeout=30)
        except asyncio.TimeoutError as exc:
            raise ElicitClientError("Gateway did not respond to handshake within 30s") from exc
        except Exception as exc:
            raise ElicitClientError(f"Connection lost during handshake: {exc}") from exc

        if isinstance(resp_raw, bytes):
            raise ElicitClientError("Unexpected binary response during handshake")

        data: dict[str, Any] = json.loads(resp_raw)

        if data.get("type") == "error":
            detail = data.get("detail", "unknown error")
            raise ElicitClientError(f"Gateway handshake error: {detail}")

        if data.get("type") != "session_ready":
            raise ElicitClientError(f"Unexpected handshake response: {data}")

        self.session_id = data.get("session_id", self._init_session_id)

    async def close(self) -> None:
        """Close the WebSocket connection."""
        if self._closed:
            return
        self._closed = True
        if self._listener_task is not None:
            self._listener_task.cancel()
            try:
                await self._listener_task
            except asyncio.CancelledError:
                pass
            self._listener_task = None
        if self._ws is not None:
            await self._ws.close()

    # ------------------------------------------------------------------
    # Event dispatch
    # ------------------------------------------------------------------

    def _dispatch_event(self, event: RealtimeSessionEvent) -> None:
        """Route a parsed event to the appropriate accumulator handler and update session state."""
        if isinstance(event, ContextSnapshotEvent):
            self.context.on_context_snapshot(event)
        elif isinstance(event, ContextUpdateEvent):
            self.context.on_context_update(event)
        elif isinstance(event, MemoryUpdateEvent):
            self.context.on_memory_update(event)
        elif isinstance(event, ContextStatusEvent):
            self.context.on_context_status(event)
        elif isinstance(event, SessionInitEvent):
            self.context.on_session_init(event)
        elif isinstance(event, TranscriptEvent):
            self.context.on_transcript(event)
        elif isinstance(event, StatusEvent):
            self.status = "processing" if event.status == "processing" else "rest"

    # ------------------------------------------------------------------
    # Background listener
    # ------------------------------------------------------------------

    def _start_listener(self) -> None:
        """Start a background task that reads events and feeds the accumulator."""
        if self._listener_task is None:
            self._listener_task = asyncio.create_task(self._listen())

    async def _listen(self) -> None:
        """Read from the WebSocket in a loop, feeding events into the context accumulator."""
        import sys

        while self._ws is not None and not self._closed:
            try:
                message = await self._ws.recv()
            except Exception:
                break

            if isinstance(message, bytes):
                print(f"[_listen] received binary frame ({len(message)} bytes)", file=sys.stderr)
                continue

            try:
                data: dict[str, Any] = json.loads(message)
                print(f"[_listen] received event: {data}", file=sys.stderr)
                event = _parse_event(data)
            except Exception as exc:
                print(f"[_listen] failed to parse event: {exc}", file=sys.stderr)
                continue

            if event is None:
                print(f"[_listen] unknown event type: {data.get('type')}", file=sys.stderr)
                continue

            self._dispatch_event(event)

            if isinstance(event, (SessionEndedEvent, ErrorEvent)):
                break

    # ------------------------------------------------------------------
    # Flush / Override
    # ------------------------------------------------------------------

    def flush(self) -> dict[str, str]:
        """Return the current context as a dict and reset all state.

        Keys: ``scene_facts``, ``system_prompt``, ``episodes``, ``transcript``.
        Each value is a plain string (empty string if nothing in that section).
        """
        context = self.context.build_context_dict()
        self.context.reset()
        return context

    async def override(self) -> None:
        """Send a flush command to the server to request fresh context data.

        This sends ``{"type": "flush"}`` over the WebSocket, which tells the
        gateway to re-run retrieval and push updated context.
        """
        if self._ws is None or self._closed:
            raise ElicitClientError("Session is not connected")
        try:
            await self._ws.send(json.dumps({"type": "flush"}))
        except Exception as exc:
            raise ElicitClientError(f"Failed to send override flush: {exc}") from exc

    async def send_assistant_message(self, text: str) -> None:
        """Send an assistant message to the gateway for transcript storage.

        Use this when ``generation=False`` to feed your own LLM's response
        back into the session.  The agent will record it in STM as an
        assistant turn, publish ``ASSISTANT_TRANSCRIPT_DONE``, and push a
        ``MEMORY_UPDATE`` with the updated transcript.

        Wire format::

            {"type": "assistant_message", "text": "The response text"}

        Args:
            text: The assistant's response text to send.
        """
        if self._ws is None or self._closed:
            raise ElicitClientError("Session is not connected")
        try:
            await self._ws.send(json.dumps({"type": "assistant_message", "text": text}))
        except Exception as exc:
            raise ElicitClientError(f"Failed to send assistant message: {exc}") from exc

    async def send_user_message(self, text: str, speaker: str = "User") -> None:
        """Send a text-based user message to the gateway.

        Use this to inject a typed/text user message into the session
        (as opposed to audio captured by the microphone).  The agent will
        record it in STM as a user turn attributed to ``speaker`` and
        push a ``MEMORY_UPDATE`` with the updated transcript.

        Wire format::

            {"type": "user_message", "text": "...", "speaker": "Jordan"}

        Args:
            text: The user's message text.
            speaker: Speaker name for STM attribution (default ``"User"``).
        """
        if self._ws is None or self._closed:
            raise ElicitClientError("Session is not connected")
        try:
            await self._ws.send(json.dumps({
                "type": "user_message",
                "text": text,
                "speaker": speaker,
            }))
        except Exception as exc:
            raise ElicitClientError(f"Failed to send user message: {exc}") from exc

    # ------------------------------------------------------------------
    # Sending media
    # ------------------------------------------------------------------

    @property
    def alive(self) -> bool:
        """``True`` if the connection is open and :meth:`close` has not been called."""
        return self._ws is not None and not self._closed

    @property
    def turn_id(self) -> Optional[int]:
        """The latest turn_id from any event."""
        return self.context.turn_id

    @property
    def working_memory(self) -> Optional[SnapshotWorkingMemory]:
        """The latest working memory from CONTEXT_SNAPSHOT.

        Returns ``None`` if only legacy events have been received.
        """
        return self.context.snapshot_working_memory

    @property
    def short_term_memory(self) -> Optional[SnapshotShortTermMemory]:
        """The latest short-term memory from CONTEXT_SNAPSHOT."""
        return self.context.snapshot_short_term_memory

    @property
    def long_term_memory(self) -> Optional[LongTermMemory]:
        """The latest long-term memory from CONTEXT_SNAPSHOT."""
        return self.context.long_term_memory

    def render_for_prompt(self) -> str:
        """Build an LLM-ready prompt string from the latest context.

        Delegates to :meth:`ContextAccumulator.build_llm_prompt`.
        """
        return self.context.build_llm_prompt()

    async def send_audio(self, pcm: bytes) -> None:
        """Send a raw PCM audio frame (16-bit mono 16 kHz).

        The data is prefixed with the ``0x01`` audio frame marker
        before being sent over the wire.
        """
        if self._ws is None or self._closed:
            raise ElicitClientError("Session is not connected")
        try:
            await self._ws.send(bytes([FRAME_AUDIO]) + pcm)
        except Exception as exc:
            raise ElicitClientError(f"Failed to send audio: {exc}") from exc

    async def send_video(
        self,
        data: bytes,
        *,
        width: Optional[int] = None,
        height: Optional[int] = None,
        format: Optional[str] = None,
    ) -> None:
        """Send a video frame.

        Can send either a pre-encoded JPEG frame or raw pixel bytes with
        format metadata so the server can decode/compress as needed.

        **JPEG mode** (default)::

            await session.send_video(jpeg_bytes)

        **Raw pixel mode**::

            await session.send_video(
                raw_bytes, width=640, height=480, format="RGB"
            )

        Wire format
        -----------
        JPEG:  ``0x02 | 0x00 | <jpeg bytes>``

        Raw:   ``0x02 | 0x01 | width(u16 BE) | height(u16 BE) |
                fmt_len(u8) | fmt_str | <raw pixel bytes>``
        """
        if self._ws is None or self._closed:
            raise ElicitClientError("Session is not connected")

        raw_mode = width is not None or height is not None or format is not None
        if raw_mode:
            if width is None or height is None or format is None:
                raise ElicitClientError(
                    "width, height, and format are all required for raw video frames"
                )
            fmt_bytes = format.encode("ascii")
            if len(fmt_bytes) > 255:
                raise ElicitClientError("format string too long (max 255 bytes)")
            header = struct.pack(">HHB", width, height, len(fmt_bytes))
            payload = (
                bytes([FRAME_VIDEO, VIDEO_SUB_RAW])
                + header
                + fmt_bytes
                + data
            )
        else:
            payload = bytes([FRAME_VIDEO, VIDEO_SUB_JPEG]) + data

        try:
            await self._ws.send(payload)
        except Exception as exc:
            raise ElicitClientError(f"Failed to send video: {exc}") from exc

    # ------------------------------------------------------------------
    # Receiving events
    # ------------------------------------------------------------------

    async def recv(self) -> Optional[RealtimeSessionEvent]:
        """Receive and parse the next server event.

        Returns ``None`` for binary frames (agent audio) or if the
        connection is closed.
        """
        if self._ws is None or self._closed:
            return None

        try:
            message = await self._ws.recv()
        except Exception:
            return None

        if isinstance(message, bytes):
            return None

        data: dict[str, Any] = json.loads(message)
        event = _parse_event(data)

        if event is None:
            return None

        self._dispatch_event(event)
        return event

    # ------------------------------------------------------------------
    # Async iteration
    # ------------------------------------------------------------------

    def __aiter__(self) -> AsyncIterator[RealtimeSessionEvent]:
        return self

    async def __anext__(self) -> RealtimeSessionEvent:
        while True:
            if self._ws is None or self._closed or self._iter_done:
                raise StopAsyncIteration

            try:
                message = await self._ws.recv()
            except Exception as exc:
                raise StopAsyncIteration from exc

            if isinstance(message, bytes):
                continue

            data: dict[str, Any] = json.loads(message)
            event = _parse_event(data)

            if event is None:
                continue

            self._dispatch_event(event)

            if isinstance(event, (SessionEndedEvent, ErrorEvent)):
                self._iter_done = True
                return event

            return event

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> AsyncRealtimeSession:
        await self._connect()
        if self._auto_listen:
            self._start_listener()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()
