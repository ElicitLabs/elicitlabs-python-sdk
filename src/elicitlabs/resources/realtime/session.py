from __future__ import annotations

import re
import json
import struct
import asyncio
import warnings
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

    # ------------------------------------------------------------------
    # Atomic prompt renderers
    # ------------------------------------------------------------------

    def prompt_scene(self) -> str:
        """Render everything from camera + voice perception.

        Includes speakers (face/voice identification), detected objects,
        and the natural language scene description from the vision pipeline.

        Returns an empty string if no perception data is available.
        """
        wm = self.snapshot_working_memory
        if wm is None:
            return ""

        parts: list[str] = []

        if wm.speakers:
            parts.append("## People Present")
            for s in wm.speakers:
                parts.append(f"- {s.description or s.name or '?'}")

        if wm.objects:
            parts.append("\n## Objects in Scene")
            for o in wm.objects:
                parts.append(f"- {o.description or o.label or '?'}")

        if wm.scene:
            parts.append(f"\n## Scene Description\n{wm.scene}")

        return "\n".join(parts)

    def prompt_working_memory(self) -> str:
        """Render cognitive working memory: summary, topics, and known people.

        Does NOT include perception data (speakers/objects/scene) —
        use :meth:`prompt_scene` for that.

        Returns an empty string if no working memory data is available.
        """
        wm = self.snapshot_working_memory
        if wm is None:
            return ""

        parts: list[str] = []

        if wm.conversation_summary:
            parts.append(f"## Conversation Summary\n{wm.conversation_summary}")

        if wm.topics:
            parts.append(f"\n## Topics\n{', '.join(wm.topics)}")

        if wm.people:
            parts.append("\n## People")
            for p in wm.people:
                parts.append(f"- {p.name or '?'} [{p.role or '?'}]: {p.context or ''}")

        return "\n".join(parts)

    def prompt_transcript(self) -> str:
        """Render the conversation transcript from short-term memory.

        Returns an empty string if no transcript data is available.
        """
        stm = self.snapshot_short_term_memory
        if stm is None or not stm.messages:
            return ""

        parts: list[str] = ["## Transcript"]
        for msg in stm.messages:
            speaker = msg.speaker or msg.role or "?"
            content = msg.content or ""
            parts.append(f"{speaker}: {content}")

        return "\n".join(parts)

    def prompt_memories(self) -> str:
        """Render long-term memories: episodic events, preferences, and identity facts.

        Returns an empty string if no long-term memory data is available.
        """
        ltm = self.long_term_memory
        if ltm is None:
            return ""

        has_any = ltm.episodic or ltm.preference or ltm.identity
        if not has_any:
            return ""

        parts: list[str] = ["## Memories"]
        for mem in (ltm.episodic or []):
            parts.append(f"- [Episode] {mem}")
        for mem in (ltm.preference or []):
            parts.append(f"- [Preference] {mem}")
        for mem in (ltm.identity or []):
            parts.append(f"- [Identity] {mem}")

        return "\n".join(parts)

    def prompt_cross_session(self) -> str:
        """Render prior session context from SESSION_INIT.

        Includes transcript segments and entity observations from recent
        sessions.  Returns an empty string if no cross-session data exists.
        """
        if not self.stm_prior_transcripts and not self.stm_prior_entities:
            return ""

        parts: list[str] = ["## Prior Session Context"]

        if self.stm_prior_transcripts:
            parts.append("\n### Recent Transcripts")
            for t in self.stm_prior_transcripts:
                speaker = t.speaker or "?"
                text = t.text or ""
                parts.append(f"- {speaker}: {text}")

        if self.stm_prior_entities:
            parts.append("\n### Known Entities")
            for e in self.stm_prior_entities:
                name = e.entity_name or "?"
                modality = e.modality or "unknown"
                parts.append(f"- {name} ({modality})")

        return "\n".join(parts)

    # ------------------------------------------------------------------
    # Composed prompt methods
    # ------------------------------------------------------------------

    def prompt_full(self) -> str:
        """Build a complete prompt from all available context.

        Composes :meth:`prompt_scene`, :meth:`prompt_working_memory`,
        :meth:`prompt_memories`, and :meth:`prompt_transcript`.

        Cross-session context is excluded by default — use
        :meth:`prompt_cross_session` or :meth:`build_messages` to include it.

        Returns ``"(no context available)"`` if all sections are empty.
        """
        sections = [
            self.prompt_scene(),
            self.prompt_working_memory(),
            self.prompt_memories(),
            self.prompt_transcript(),
        ]
        sections = [s for s in sections if s]
        return "\n\n".join(sections) if sections else "(no context available)"

    def build_messages(
        self,
        user_question: str = "Respond based on the context above.",
        *,
        include_scene: bool = True,
        include_working_memory: bool = True,
        include_memories: bool = True,
        include_transcript: bool = True,
        include_cross_session: bool = False,
    ) -> list[dict[str, str]]:
        """Return an OpenAI-compatible messages list with selectable sections.

        The system message is composed from whichever sections are enabled.
        Transcript messages are expanded as individual user/assistant turns.

        Args:
            user_question: Appended as the final user message.
            include_scene: Include speakers, objects, scene description.
            include_working_memory: Include summary, topics, people.
            include_memories: Include long-term memories.
            include_transcript: Expand STM messages as conversation turns.
            include_cross_session: Include prior session context.
        """
        system_parts: list[str] = []
        if include_cross_session:
            s = self.prompt_cross_session()
            if s:
                system_parts.append(s)
        if include_scene:
            s = self.prompt_scene()
            if s:
                system_parts.append(s)
        if include_working_memory:
            s = self.prompt_working_memory()
            if s:
                system_parts.append(s)
        if include_memories:
            s = self.prompt_memories()
            if s:
                system_parts.append(s)

        messages: list[dict[str, str]] = []
        if system_parts:
            messages.append({"role": "system", "content": "\n\n".join(system_parts)})

        if include_transcript:
            stm = self.snapshot_short_term_memory
            if stm and stm.messages:
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

    # ------------------------------------------------------------------
    # Structured getters
    # ------------------------------------------------------------------

    def get_scene(self) -> dict[str, Any]:
        """Return scene perception data as a structured dict.

        Keys: ``scene``, ``speakers``, ``objects``.
        """
        wm = self.snapshot_working_memory
        return {
            "scene": wm.scene if wm else None,
            "speakers": [s.model_dump() for s in (wm.speakers or [])] if wm else [],
            "objects": [o.model_dump() for o in (wm.objects or [])] if wm else [],
        }

    def get_working_memory(self) -> dict[str, Any]:
        """Return cognitive working memory as a structured dict.

        Keys: ``summary``, ``topics``, ``people``.
        """
        wm = self.snapshot_working_memory
        return {
            "summary": wm.conversation_summary if wm else None,
            "topics": list(wm.topics or []) if wm else [],
            "people": [p.model_dump() for p in (wm.people or [])] if wm else [],
        }

    def get_transcript(self) -> list[dict[str, Any]]:
        """Return the conversation transcript as a list of message dicts."""
        stm = self.snapshot_short_term_memory
        if stm and stm.messages:
            return [m.model_dump() for m in stm.messages]
        return []

    def get_memories(self) -> dict[str, list[str]]:
        """Return long-term memories as a structured dict.

        Keys: ``episodic``, ``preference``, ``identity``.
        """
        ltm = self.long_term_memory
        return {
            "episodic": list(ltm.episodic or []) if ltm else [],
            "preference": list(ltm.preference or []) if ltm else [],
            "identity": list(ltm.identity or []) if ltm else [],
        }

    # ------------------------------------------------------------------
    # Legacy methods (deprecated)
    # ------------------------------------------------------------------

    def build_llm_prompt(self) -> str:
        """.. deprecated:: Use :meth:`prompt_full` instead."""
        warnings.warn("build_llm_prompt() is deprecated, use prompt_full() instead", DeprecationWarning, stacklevel=2)
        return self.prompt_full()

    def build_llm_messages(
        self,
        user_question: str = "Respond based on the context above.",
    ) -> list[dict[str, str]]:
        """.. deprecated:: Use :meth:`build_messages` instead."""
        warnings.warn("build_llm_messages() is deprecated, use build_messages() instead", DeprecationWarning, stacklevel=2)
        return self.build_messages(user_question)

    def build_context_dict(self) -> dict[str, str]:
        """.. deprecated:: Use :meth:`get_scene`, :meth:`get_working_memory`,
        :meth:`get_transcript`, :meth:`get_memories` instead.

        Legacy card-based context dict. Kept for backward compatibility.
        """
        warnings.warn("build_context_dict() is deprecated, use get_scene()/get_working_memory()/get_transcript()/get_memories() instead", DeprecationWarning, stacklevel=2)
        all_cards = self.cards
        scene_facts = [c for c in all_cards if c.type in self.SCENE_FACT_TYPES]
        all_system = [c for c in all_cards if c.type in self.SYSTEM_PROMPT_TYPES]
        episodes = [c for c in all_cards if c.type in self.EPISODE_TYPES]

        new_system: list[ContextCard] = []
        for c in all_system:
            key = self._dedup_key(c)
            if key not in self._flushed_system_prompt:
                new_system.append(c)
                self._flushed_system_prompt.add(key)

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
        """.. deprecated:: Use :meth:`prompt_full` instead.

        Legacy card-based context string. Kept for backward compatibility.
        """
        warnings.warn("build_context_string() is deprecated, use prompt_full() instead", DeprecationWarning, stacklevel=2)
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
        scene_understanding: Optional[bool] = None,
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
        self._scene_understanding = scene_understanding

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
        if self._scene_understanding is not None:
            init_msg["scene_understanding"] = self._scene_understanding

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

    def flush(self) -> dict[str, Any]:
        """Return the current understanding as a dict and reset all state.

        Returns the same dict as :meth:`get_understanding`.
        """
        context = self.get_understanding()
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

    @property
    def scene(self) -> Optional[str]:
        """Natural language scene description from the vision pipeline.

        Returns the ``scene`` string from the latest
        ``CONTEXT_SNAPSHOT`` working memory, or ``None`` when scene
        understanding is disabled or no snapshot has been received yet.
        """
        wm = self.context.snapshot_working_memory
        return wm.scene if wm is not None else None

    # ------------------------------------------------------------------
    # Prompt builders (delegate to ContextAccumulator)
    # ------------------------------------------------------------------

    def prompt_scene(self) -> str:
        """Everything from camera + voice: speakers, objects, scene description."""
        return self.context.prompt_scene()

    def prompt_working_memory(self) -> str:
        """Cognitive state: conversation summary, topics, known people."""
        return self.context.prompt_working_memory()

    def prompt_transcript(self) -> str:
        """Conversation transcript from short-term memory."""
        return self.context.prompt_transcript()

    def prompt_memories(self) -> str:
        """Long-term memories: episodic, preference, identity."""
        return self.context.prompt_memories()

    def prompt_cross_session(self) -> str:
        """Prior session context from SESSION_INIT."""
        return self.context.prompt_cross_session()

    def prompt_full(self) -> str:
        """Complete prompt from all sections (scene + WM + memories + transcript)."""
        return self.context.prompt_full()

    def build_messages(
        self,
        user_question: str = "Respond based on the context above.",
        *,
        include_scene: bool = True,
        include_working_memory: bool = True,
        include_memories: bool = True,
        include_transcript: bool = True,
        include_cross_session: bool = False,
    ) -> list[dict[str, str]]:
        """OpenAI-compatible messages list with selectable context sections."""
        return self.context.build_messages(
            user_question,
            include_scene=include_scene,
            include_working_memory=include_working_memory,
            include_memories=include_memories,
            include_transcript=include_transcript,
            include_cross_session=include_cross_session,
        )

    # ------------------------------------------------------------------
    # Structured getters (delegate to ContextAccumulator)
    # ------------------------------------------------------------------

    def get_understanding(self) -> dict[str, Any]:
        """Return everything the SDK knows right now as a structured dict.

        Combines scene, working memory, transcript, and memories into
        a single dict. For individual sections, use :meth:`get_scene`,
        :meth:`get_working_memory`, etc. on ``session.context``.
        """
        scene = self.context.get_scene()
        wm = self.context.get_working_memory()
        return {
            **scene,
            **wm,
            "transcript": self.context.get_transcript(),
            "memories": self.context.get_memories(),
        }

    # ------------------------------------------------------------------
    # Deprecated methods
    # ------------------------------------------------------------------

    def render_understanding(self) -> str:
        """.. deprecated:: Use :meth:`prompt_full` instead."""
        warnings.warn("render_understanding() is deprecated, use prompt_full() instead", DeprecationWarning, stacklevel=2)
        return self.context.prompt_full()

    def render_for_prompt(self) -> str:
        """.. deprecated:: Use :meth:`prompt_full` instead."""
        warnings.warn("render_for_prompt() is deprecated, use prompt_full() instead", DeprecationWarning, stacklevel=2)
        return self.context.prompt_full()

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
