from __future__ import annotations

import json
import asyncio
from typing import Any, List, Optional, AsyncIterator

from ..._exceptions import ElicitClientError
from ...types.realtime.session_events import (
    ErrorEvent,
    ContextCard,
    StatusEvent,
    TranscriptEvent,
    SessionEndedEvent,
    SessionReadyEvent,
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

SAMPLE_RATE: int = 16_000
CHANNELS: int = 1
BYTES_PER_SAMPLE: int = 2
CHUNK_DURATION_MS: int = 20
SAMPLES_PER_CHUNK: int = SAMPLE_RATE * CHUNK_DURATION_MS // 1000
BYTES_PER_CHUNK: int = SAMPLES_PER_CHUNK * CHANNELS * BYTES_PER_SAMPLE

_EVENT_TYPE_MAP: dict[str, type[Any]] = {
    "session_ready": SessionReadyEvent,
    "transcript": TranscriptEvent,
    "context_update": ContextUpdateEvent,
    "context_snapshot": ContextUpdateEvent,
    "session_ended": SessionEndedEvent,
    "error": ErrorEvent,
    "status": StatusEvent,
}

_TYPE_ALIASES: dict[str, str] = {
    "context_snapshot": "context_update",
}


def _parse_event(raw: dict[str, Any]) -> RealtimeSessionEvent:
    event_type = raw.get("type", "")
    normalized = event_type.lower()
    canonical = _TYPE_ALIASES.get(normalized, normalized)
    cls = _EVENT_TYPE_MAP.get(normalized)
    if cls is not None:
        raw = {**raw, "type": canonical}
        return cls.model_validate(raw)  # type: ignore[return-value]
    return SessionEndedEvent.model_validate({"type": "session_ended", "reason": f"unknown event: {event_type}"})


class ContextAccumulator:
    """Collects ``context_update`` events and builds a unified context string
    that can be injected into your own LLM calls."""

    cards: List[ContextCard]
    messages: List[dict[str, object]]
    transcripts: List[str]

    def __init__(self) -> None:
        self.cards = []
        self.messages = []
        self.transcripts = []
        self._context_version = 0

    def reset(self) -> None:
        """Clear all accumulated state."""
        self.cards.clear()
        self.messages.clear()
        self.transcripts.clear()
        self._context_version = 0

    def on_context_update(self, event: ContextUpdateEvent) -> None:
        version = event.context_version or 0
        self._context_version = max(self._context_version, version)

        for op in event.ops or []:
            if op.op == "add" and op.card is not None:
                self.cards.append(op.card)

        for msg in event.messages or []:
            self.messages.append(msg)

    def on_transcript(self, event: TranscriptEvent) -> None:
        text = event.text or ""
        if text.strip():
            self.transcripts.append(text)

    def build_context_string(self) -> str:
        """Build a single context string from all accumulated cards,
        ready for injection as a system message in your own LLM."""
        sections: list[str] = []

        episodic = [c for c in self.cards if c.type == "episodic"]
        preferences = [c for c in self.cards if c.type == "preference"]
        identity = [c for c in self.cards if c.type == "identity"]
        visual = [
            c
            for c in self.cards
            if c.type in ("face_identity", "speaker_identity", "scene_fact", "attention_target")
        ]

        if episodic:
            lines = [f"  - {c.claim or ''}" for c in episodic]
            sections.append("Episodic Memories:\n" + "\n".join(lines))

        if preferences:
            lines = [f"  - {c.claim or ''}" for c in preferences]
            sections.append("User Preferences:\n" + "\n".join(lines))

        if identity:
            lines = [f"  - {c.claim or ''}" for c in identity]
            sections.append("Identity Facts:\n" + "\n".join(lines))

        if visual:
            lines = [f"  - [{c.type}] {c.claim or ''}" for c in visual]
            sections.append("Visual Observations:\n" + "\n".join(lines))

        if self.transcripts:
            sections.append("Transcript:\n  " + " ".join(self.transcripts))

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
        while self._ws is not None and not self._closed:
            try:
                message = await self._ws.recv()
            except Exception:
                break

            if isinstance(message, bytes):
                continue

            data: dict[str, Any] = json.loads(message)
            event = _parse_event(data)

            if isinstance(event, ContextUpdateEvent):
                self.context.on_context_update(event)
            elif isinstance(event, TranscriptEvent):
                self.context.on_transcript(event)
            elif isinstance(event, StatusEvent):
                self.status = "processing" if event.status == "processing" else "rest"

            if isinstance(event, (SessionEndedEvent, ErrorEvent)):
                break

    # ------------------------------------------------------------------
    # Flush / Override
    # ------------------------------------------------------------------

    def flush(self) -> str:
        """Drain the accumulated context and reset the accumulator.

        Returns the context string built from all cards and transcripts
        collected since the last flush (or since the session started).
        """
        context_string = self.context.build_context_string()
        self.context.reset()
        return context_string

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

    async def send_video(self, jpeg: bytes) -> None:
        """Send a JPEG video frame.

        The data is prefixed with the ``0x02`` video frame marker
        before being sent over the wire.
        """
        if self._ws is None or self._closed:
            raise ElicitClientError("Session is not connected")
        try:
            await self._ws.send(bytes([FRAME_VIDEO]) + jpeg)
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

        if isinstance(event, ContextUpdateEvent):
            self.context.on_context_update(event)
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

            if isinstance(event, ContextUpdateEvent):
                self.context.on_context_update(event)
            elif isinstance(event, TranscriptEvent):
                self.context.on_transcript(event)

            if isinstance(event, SessionEndedEvent) or isinstance(event, ErrorEvent):
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
