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

    audio_config: Optional[AudioConfig]
    """Configuration overrides for audio generation"""

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    image_config: Optional[ImageConfig]
    """Configuration overrides for image generation"""

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    modalities: SequenceNotStr[str]
    """List of desired outputs: 'text', 'image', 'audio'"""

    model: str
    """LLM model to use for generation"""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    stream: bool
    """Enable streaming response (SSE)"""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before answering"""


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
    """Voice to use (alloy, echo, fable, onyx, nova, shimmer)"""


class ImageConfig(TypedDict, total=False):
    """Configuration overrides for image generation"""

    model: Optional[str]
    """Image generation model (e.g., gemini-3-flash, dall-e-3)"""

    seed: Optional[int]
    """Random seed for reproducibility"""

    size: Optional[str]
    """Image dimensions"""
