# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ChatCreateCompletionParams", "Message", "MessageContentUnionMember1", "AudioConfig", "ImageConfig"]


class ChatCreateCompletionParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """List of messages (system, user, assistant) with text, images, video, or audio"""

    user_id: Required[str]
    """The end-user ID"""

    agent_mode: bool
    """Enable agent mode for multi-step tool-calling workflows.

    When True (or when the classifier detects agentic intent), the request is
    handled by the agent service which can orchestrate memory retrieval, video
    analysis, segmentation, image generation, and more.
    """

    audio_config: Optional[AudioConfig]
    """Configuration overrides for audio generation"""

    auto_detect_agent: bool
    """
    When True (default), the modality classifier may auto-route to agent mode even
    if not explicitly requested. Set to False for deterministic routing (e.g.
    Instagram integration) where you want only the modalities you specify.
    """

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    history_limit: int
    """Maximum number of prior turns to load when load_history is True"""

    image_config: Optional[ImageConfig]
    """Configuration overrides for image generation"""

    load_history: bool
    """
    When True, loads prior conversation turns from the database using session_id and
    prepends them to messages. Use this for stateless callers (e.g. Instagram
    webhooks) that send only the latest message and rely on server-side history.
    Requires session_id to be set.
    """

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    modalities: SequenceNotStr[str]
    """List of desired outputs: 'text', 'image', 'audio'.

    When 'agent' is included or agent_mode is True, the agent loop handles the
    request.
    """

    model: str
    """LLM model to use for generation"""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    skip_initial_retrieval: bool
    """
    When True, the agent skips the automatic memory retrieval at the start of each
    turn. Use this when the caller has already embedded user context in the system
    prompt (e.g. Instagram integration) and wants the agent to retrieve memories
    on-demand via the tool instead.
    """

    stream: bool
    """Enable streaming response (SSE)"""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before answering"""

    video_refs: Optional[Dict[str, str]]
    """
    Map of video labels (video_0, video_1, …) to GCS S3 keys from conversation
    history.
    """


class MessageContentUnionMember1(TypedDict, total=False):
    """A single content part within a multimodal message"""

    type: Required[str]
    """Content type: 'text', 'image', 'video', 'audio', or 'image_url'"""

    audio_url: Optional[Dict[str, str]]
    """Audio URL object with 'url' key"""

    content: Optional[str]
    """Base64 encoded content (for image/video/audio)"""

    format: Optional[str]
    """Asset format, e.g. png, jpeg, mp3, wav, mp4"""

    image_url: Optional[Dict[str, str]]
    """Image URL object with 'url' key (can be data:image/... base64)"""

    text: Optional[str]
    """Text content (when type='text')"""

    url: Optional[str]
    """Signed GCS URL to download the asset (expires after 24 h)"""

    video_url: Optional[Dict[str, str]]
    """Video URL object with 'url' key"""


class Message(TypedDict, total=False):
    """A single message in the conversation"""

    content: Required[Union[str, Iterable[MessageContentUnionMember1], Iterable[Dict[str, object]]]]
    """
    Message content - can be: - A simple text string - An array of content parts for
    multimodal input: [ {"type": "text", "text": "What's in this image?"}, {"type":
    "image", "content": "base64_encoded_image..."}, {"type": "image_url",
    "image_url": {"url": "data:image/jpeg;base64,..."}}, {"type": "video",
    "content": "base64_encoded_video..."}, {"type": "audio", "content":
    "base64_encoded_audio..."} ]
    """

    role: Required[str]
    """Message role: 'system', 'user', or 'assistant'"""


class AudioConfig(TypedDict, total=False):
    """Configuration overrides for audio generation"""

    audio_type: str
    """Type: 'speech' (TTS), 'music', or 'sfx'"""

    duration: Optional[float]
    """Duration in seconds for music/sfx"""

    model: Optional[str]
    """Audio generation model"""

    speed: float
    """Speech speed (0.25-4.0)"""

    voice: str
    """
    Voice to use — ElevenLabs voices (Rachel, Drew, Clyde, etc.) or OpenAI voices
    (alloy, echo, fable, onyx, nova, shimmer)
    """


class ImageConfig(TypedDict, total=False):
    """Configuration overrides for image generation"""

    model: Optional[str]
    """Image generation model (e.g., gemini-3-flash, dall-e-3)"""

    seed: Optional[int]
    """Random seed for reproducibility"""

    size: Optional[str]
    """Image dimensions"""
