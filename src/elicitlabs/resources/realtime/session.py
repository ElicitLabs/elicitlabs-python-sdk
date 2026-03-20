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
    TranscriptEvent,
    SessionEndedEvent,
    SessionInitEvent,
    SessionReadyEvent,
    MemoryUpdateEvent,
    ContextStatusEvent,
    ContextUpdateEvent,
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
    "context_snapshot": ContextUpdateEvent,
    "context_status": ContextStatusEvent,
    "session_ended": SessionEndedEvent,
    "error": ErrorEvent,
    "status": StatusEvent,
}

_TYPE_ALIASES: dict[str, str] = {
    "context_snapshot": "context_update",
}


def _parse_event(raw: dict[str, Any]) -> Optional[RealtimeSessionEvent]:
    """Parse a raw JSON dict into a typed event, or ``None`` for unknown types."""
    event_type = raw.get("type", "")
    normalized = event_type.lower()
    canonical = _TYPE_ALIASES.get(normalized, normalized)
    cls = _EVENT_TYPE_MAP.get(normalized)
    if cls is not None:
        raw = {**raw, "type": canonical}
        return cls.model_validate(raw)  # type: ignore[return-value]
    return None


class ContextAccumulator:
    """Collects ``CONTEXT_UPDATE`` and ``CONTEXT_STATUS`` events and builds a
    unified context string that can be injected into your own LLM calls.

    Maintains a **card store** keyed by ``card.id``.  Applies ``add``,
    ``update``, and ``expire`` operations sequentially.

    Cards are split into three output sections:

    * **scene_facts** — ``face_identity``, ``speaker_identity``,
      ``scene_fact``, ``attention_target``
    * **system_prompt** — ``identity``, ``preference``
    * **episodes** — ``episodic``

    Working memory is tracked from both ``CONTEXT_UPDATE`` and
    ``CONTEXT_STATUS`` events and exposed via :attr:`working_memory`.
    """

    # Card types grouped by output section
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
        """Latest working memory state from the server (from MEMORY_UPDATE or CONTEXT_UPDATE)."""

        self.short_term_memory: Optional[Any] = None
        """Latest short-term memory from MEMORY_UPDATE (speaker-attributed transcript)."""

        self.active_entities: dict[str, dict[str, str]] = {}
        """Entity presence map from the latest CONTEXT_STATUS heartbeat.
        Keyed by entity_id -> {name, modality}."""

        self.stm_prior_transcripts: List[Any] = []
        """Prior transcript segments from SESSION_INIT (cross-session context)."""

        self.stm_prior_entities: List[Any] = []
        """Prior entity observations from SESSION_INIT (cross-session context)."""

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
        if event.short_term_memory is not None:
            self.short_term_memory = event.short_term_memory
        if event.working_memory is not None:
            self.working_memory = event.working_memory

    def on_context_update(self, event: ContextUpdateEvent) -> None:
        """Process a CONTEXT_UPDATE event: apply card ops, update working memory."""
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

    def build_llm_messages(
        self,
        user_question: str = "Respond based on the context above.",
    ) -> list[dict[str, str]]:
        """Return a ``messages`` list suitable for ``openai.chat.completions.create()``
        or ``anthropic.messages.create()``."""
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

            if isinstance(event, ContextUpdateEvent):
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

        if isinstance(event, ContextUpdateEvent):
            self.context.on_context_update(event)
        elif isinstance(event, MemoryUpdateEvent):
            self.context.on_memory_update(event)
        elif isinstance(event, ContextStatusEvent):
            self.context.on_context_status(event)
        elif isinstance(event, SessionInitEvent):
            self.context.on_session_init(event)
        elif isinstance(event, TranscriptEvent):
            self.context.on_transcript(event)

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

            if isinstance(event, ContextUpdateEvent):
                self.context.on_context_update(event)
            elif isinstance(event, MemoryUpdateEvent):
                self.context.on_memory_update(event)
            elif isinstance(event, ContextStatusEvent):
                self.context.on_context_status(event)
            elif isinstance(event, SessionInitEvent):
                self.context.on_session_init(event)
            elif isinstance(event, TranscriptEvent):
                self.context.on_transcript(event)

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
