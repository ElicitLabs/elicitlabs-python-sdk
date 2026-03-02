from __future__ import annotations

from typing import List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = [
    "ContextCard",
    "ContextCardOperation",
    "ContextUpdateEvent",
    "ErrorEvent",
    "RealtimeSessionEvent",
    "SessionEndedEvent",
    "SessionReadyEvent",
    "StatusEvent",
    "TranscriptEvent",
]


class ContextCard(BaseModel):
    """A memory card retrieved by the perception + retrieval pipeline."""

    type: Optional[str] = None
    """Card type: episodic, preference, identity, face_identity, speaker_identity, scene_fact, attention_target."""

    claim: Optional[str] = None
    """The textual claim or fact represented by this card."""

    score: Optional[float] = None
    """Relevance score assigned during retrieval."""

    source: Optional[str] = None
    """Source of the memory (e.g. 'episodic_store', 'preference_store')."""

    metadata: Optional[dict[str, object]] = None
    """Additional metadata attached to the card."""


class ContextCardOperation(BaseModel):
    """An operation on a context card (add/remove/update)."""

    op: Optional[str] = None
    """Operation type: 'add', 'remove', or 'update'."""

    card: Optional[ContextCard] = None
    """The card this operation applies to."""


class SessionReadyEvent(BaseModel):
    """Emitted when the gateway has accepted the session init handshake."""

    type: Literal["session_ready"]

    session_id: Optional[str] = None


class TranscriptEvent(BaseModel):
    """Emitted when speech-to-text produces a transcript of the user's audio."""

    type: Literal["transcript"]

    text: Optional[str] = None
    """The transcribed text."""

    is_final: Optional[bool] = None
    """Whether this is a final (non-interim) transcript."""


class ContextUpdateEvent(BaseModel):
    """Emitted when the retrieval pipeline returns memory context.

    This is the primary event in ``generation=False`` mode.
    """

    type: Literal["context_update"]

    ops: Optional[List[ContextCardOperation]] = None
    """Card-level add/remove/update operations."""

    messages: Optional[List[dict[str, object]]] = None
    """Pre-formatted context messages from the server."""

    context_version: Optional[int] = None
    """Monotonically increasing context version counter."""


class SessionEndedEvent(BaseModel):
    """Emitted when the server ends the session."""

    type: Literal["session_ended"]

    reason: Optional[str] = None


class ErrorEvent(BaseModel):
    """Emitted when the server reports an error."""

    type: Literal["error"]

    detail: Optional[str] = None

    code: Optional[str] = None


class StatusEvent(BaseModel):
    """Emitted when the server reports a processing status change."""

    type: Literal["status"]

    status: Literal["processing", "done"]
    """Current pipeline status: ``processing`` while the server is working,
    ``done`` when the result is ready."""


RealtimeSessionEvent = Union[
    SessionReadyEvent,
    TranscriptEvent,
    ContextUpdateEvent,
    SessionEndedEvent,
    ErrorEvent,
    StatusEvent,
]
