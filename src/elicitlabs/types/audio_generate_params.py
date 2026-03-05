# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["AudioGenerateParams"]


class AudioGenerateParams(TypedDict, total=False):
    text_input: Required[str]
    """The prompt/description for audio generation"""

    user_id: Required[str]
    """The end-user ID"""

    audio_base64: Optional[str]
    """Base64 encoded reference audio for context"""

    audio_type: Literal["speech", "sfx", "music"]
    """Audio type: 'speech', 'sfx', or 'music'"""

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    duration: Optional[float]
    """Max duration in seconds for music/sfx"""

    image_base64: Optional[str]
    """Base64 encoded reference image for context"""

    model: str
    """Audio generation model ID"""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    seed: Optional[int]
    """Random seed for reproducibility"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    speed: float
    """Playback speed (0.5-2.0), only for speech"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""

    voice: str
    """Voice ID for TTS (alloy, echo, fable, onyx, nova, shimmer)"""
