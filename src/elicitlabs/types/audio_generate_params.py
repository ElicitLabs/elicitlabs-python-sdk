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
    """Max duration in seconds for music/sfx (Lyria 2 always generates 30s)"""

    image_base64: Optional[str]
    """Base64 encoded reference image for context"""

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    model: str
    """
    Audio generation model: 'lyria-2' (Google Lyria 2 on Vertex AI, default for
    music — 30s 48kHz WAV), 'audiocraft' (MusicGen/AudioGen on Cloud Run), or
    'eleven-turbo' (ElevenLabs TTS for speech)
    """

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    seed: Optional[int]
    """
    Random seed for deterministic generation (Lyria 2 only, cannot be combined with
    sample_count)
    """

    session_id: Optional[str]
    """Session ID for conversation context"""

    speed: float
    """Playback speed (0.5-2.0), only for speech"""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before answering"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""

    voice: str
    """Voice ID for TTS (alloy, echo, fable, onyx, nova, shimmer)"""
