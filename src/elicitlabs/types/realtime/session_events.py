from __future__ import annotations

from typing import Any, Dict, List, Union, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = [
    "ContextCard",
    "ContextCardOperation",
    "ContextStatusEvent",
    "ContextUpdateEvent",
    "ErrorEvent",
    "MemoryUpdateEvent",
    "RealtimeSessionEvent",
    "SessionEndedEvent",
    "SessionInitEvent",
    "SessionReadyEvent",
    "ShortTermMemory",
    "StmEntity",
    "StmTranscript",
    "StmTranscriptTurn",
    "StatusEvent",
    "TranscriptEvent",
    "WorkingMemory",
    "WorkingMemoryPerson",
    "WorkingMemorySceneItem",
]


class ContextCard(BaseModel):
    """A memory card retrieved by the perception + retrieval pipeline."""

    id: Optional[str] = None
    """Unique card identifier (e.g. 'card_a1b2c3d4e5f6')."""

    type: Optional[str] = None
    """Card type: episodic, preference, identity, face_identity, speaker_identity, scene_fact, attention_target."""

    about: Optional[str] = None
    """Who or what this card is about (e.g. a person's name)."""

    claim: Optional[str] = None
    """The textual claim or fact represented by this card."""

    confidence: Optional[float] = None
    """Confidence score from the perception/retrieval pipeline."""

    score: Optional[float] = None
    """Relevance score assigned during retrieval (legacy, prefer confidence)."""

    entity_id: Optional[str] = None
    """The entity UUID this card relates to."""

    tracklet_id: Optional[str] = None
    """Tracklet identifier for visual tracking (e.g. 'person_0')."""

    evidence_ts: Optional[float] = None
    """Timestamp of the evidence that produced this card."""

    created_at: Optional[float] = None
    """Timestamp when this card was created."""

    hash: Optional[str] = None
    """Deduplication hash for this card."""

    entity_name: Optional[str] = None
    """Human-readable name of the entity."""

    source: Optional[str] = None
    """Source of the memory (e.g. 'episodic_store', 'preference_store')."""

    metadata: Optional[Dict[str, object]] = None
    """Additional metadata attached to the card."""


class ContextCardOperation(BaseModel):
    """An operation on a context card (add/update/expire).

    For ``add``, the full ``card`` is provided.
    For ``update``, ``card_id`` and ``updates`` dict are provided.
    For ``expire``, ``card_id`` is provided.
    """

    op: Optional[str] = None
    """Operation type: 'add', 'update', or 'expire'."""

    card: Optional[ContextCard] = None
    """The full card (present on 'add' ops)."""

    card_id: Optional[str] = None
    """Card ID to target (present on 'update' and 'expire' ops)."""

    updates: Optional[Dict[str, object]] = None
    """Fields to merge into the existing card (present on 'update' ops)."""


class WorkingMemoryPerson(BaseModel):
    """A person tracked in working memory (from graduation LLM)."""

    name: Optional[str] = None
    """Person's name."""

    role: Optional[str] = None
    """Role: 'speaker', 'mentioned', or 'user'."""

    context: Optional[str] = None
    """What the system knows about this person in the current conversation."""


class WorkingMemorySceneItem(BaseModel):
    """A real-time perception item (person/object currently visible).

    Salience decays over time from 1.0 -> 0.0.
    """

    type: Optional[str] = None
    """Item type: 'person', 'scene_object', etc."""

    content: Optional[str] = None
    """Human-readable label (e.g. person name, object type)."""

    salience: Optional[float] = None
    """Current salience score (0-1), decays over time."""

    entity_id: Optional[str] = None
    """Associated entity UUID."""

    modality: Optional[str] = None
    """Detection modality (e.g. 'face', 'voice')."""


class WorkingMemory(BaseModel):
    """The server's current working memory state.

    ``conversation_summary`` and ``people`` are populated by the graduation
    LLM (fires every ~10 STM turns).  ``scene`` comes from the real-time
    perception pipeline (face/object detection) with live salience decay.
    """

    conversation_summary: Optional[str] = None
    """Running narrative of the full conversation (updated every ~10 turns by graduation)."""

    topic_summaries: Optional[List[str]] = None
    """Key topics discussed (max ~8)."""

    people: Optional[List[WorkingMemoryPerson]] = None
    """Everyone identified — role is 'speaker', 'mentioned', or 'user'."""

    scene: Optional[List[WorkingMemorySceneItem]] = None
    """Real-time perception items (people/objects currently visible)."""


class StmTranscript(BaseModel):
    """A prior transcript segment from short-term memory (cross-session)."""

    text: Optional[str] = None
    speaker: Optional[str] = None
    entity_ids: Optional[List[str]] = None
    session_id: Optional[str] = None
    ts: Optional[float] = None


class StmEntity(BaseModel):
    """A prior entity observation from short-term memory (cross-session)."""

    entity_id: Optional[str] = None
    entity_name: Optional[str] = None
    modality: Optional[str] = None
    confidence: Optional[float] = None
    session_id: Optional[str] = None
    ts: Optional[float] = None


class SessionReadyEvent(BaseModel):
    """Emitted when the gateway has accepted the session init handshake."""

    type: Literal["session_ready"]

    session_id: Optional[str] = None


class SessionInitEvent(BaseModel):
    """Emitted once at connection time with prior cross-session context from STM.

    Contains transcripts and entity observations from recent sessions.
    Only sent if there is prior data.
    """

    type: Literal["session_init"]

    session_id: Optional[str] = None

    stm_prior_transcripts: Optional[List[StmTranscript]] = None
    """Transcript segments from recent prior sessions."""

    stm_prior_entities: Optional[List[StmEntity]] = None
    """Entity observations from recent prior sessions."""


class StmTranscriptTurn(BaseModel):
    """A single speaker-attributed turn in the STM transcript."""

    turn_id: Optional[str] = None
    """Turn identifier."""

    role: Optional[str] = None
    """Role: 'user' or 'assistant'."""

    content: Optional[str] = None
    """What was said."""

    speaker: Optional[str] = None
    """Speaker name (e.g. 'Jordan', 'Assistant')."""

    ts: Optional[float] = None
    """Timestamp."""


class ShortTermMemory(BaseModel):
    """Short-term memory: the live conversation transcript."""

    transcript: Optional[List[StmTranscriptTurn]] = None
    """Speaker-attributed conversation turns."""


class MemoryUpdateEvent(BaseModel):
    """Emitted on every turn boundary and after every assistant response.

    Carries both STM (speaker-attributed transcript) and structured WM
    (scene items, topics, LLM summaries).  ``conversation_summary`` and
    ``people`` in working_memory will be empty until the first graduation
    fires (after ~10 turns or 2 minutes).
    """

    type: Literal["memory_update"]

    session_id: Optional[str] = None
    """Session identifier."""

    turn_id: Optional[int] = None
    """Turn counter for this event."""

    short_term_memory: Optional[ShortTermMemory] = None
    """Live conversation transcript (speaker-attributed turns)."""

    working_memory: Optional[WorkingMemory] = None
    """Structured working memory: summary, topics, people, scene."""


class TranscriptEvent(BaseModel):
    """Emitted when speech-to-text produces a transcript of the user's audio."""

    type: Literal["transcript"]

    text: Optional[str] = None
    """The transcribed text."""

    is_final: Optional[bool] = None
    """Whether this is a final (non-interim) transcript."""


class ContextUpdateEvent(BaseModel):
    """Emitted every ~100ms when there are new or changed cards.

    This is the primary data delivery event. All perception results,
    retrieval results, and identity promotions flow through here.
    """

    type: Literal["context_update"]

    session_id: Optional[str] = None
    """Session identifier."""

    turn_id: Optional[int] = None
    """Turn counter for this event."""

    ops: Optional[List[ContextCardOperation]] = None
    """Card-level add/update/expire operations."""

    messages: Optional[List[Any]] = None
    """Pre-formatted messages suitable for display (strings or dicts)."""

    context_version: Optional[int] = None
    """Monotonically increasing context version counter."""

    working_memory: Optional[WorkingMemory] = None
    """Current working memory state — who/what the agent is attending to."""


class ContextStatusEvent(BaseModel):
    """Periodic lightweight heartbeat with entity presence and working memory.

    Fired approximately every 5 qualifying turns. Contains no card contents —
    use as a consistency checkpoint to reconcile local state.
    """

    type: Literal["context_status"]

    session_id: Optional[str] = None
    """Session identifier."""

    turn_id: Optional[int] = None
    """Turn counter for this event."""

    context_version: Optional[int] = None
    """Monotonically increasing context version counter."""

    active_entities: Optional[Dict[str, Dict[str, str]]] = None
    """Map of entity_id -> {name, modality} for currently present entities."""

    working_memory: Optional[WorkingMemory] = None
    """Current working memory state."""


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
    SessionInitEvent,
    MemoryUpdateEvent,
    TranscriptEvent,
    ContextUpdateEvent,
    ContextStatusEvent,
    SessionEndedEvent,
    ErrorEvent,
    StatusEvent,
]
