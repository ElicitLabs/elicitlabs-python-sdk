# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["InferenceGenerateMultimodalityCompletionParams"]


class InferenceGenerateMultimodalityCompletionParams(TypedDict, total=False):
    user_id: Required[str]
    """Unique identifier for the user (always required)"""

    audio_base64: Optional[str]
    """Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)"""

    audio_duration: Optional[float]
    """Duration in seconds for music/sfx generation.

    Default: 5s for sfx, 10s for music
    """

    audio_type: Literal["tts", "music", "sfx"]
    """
    Type of audio output: 'tts' for text-to-speech, 'music' for AI music, 'sfx' for
    sound effects
    """

    context: Optional[str]
    """Additional context for the question"""

    disabled_learning: bool
    """Whether to disable learning/ingestion of the multimodal content"""

    image_base64: Optional[str]
    """Base64 encoded image content"""

    max_reasoning_iterations: int
    """Maximum repair iterations in reasoning loop"""

    model: Optional[str]
    """LLM model to use for generating the response"""

    num_images: int
    """Number of images to generate (each with a different seed for variation).

    Only used when output_type='image'
    """

    output_type: Literal["text", "audio", "image"]
    """
    Output type: 'text' for text only, 'audio' for TTS audio, 'image' for
    AI-generated image
    """

    persona_id: Optional[str]
    """Optional persona ID.

    If provided, inference uses this persona's context instead of the user
    """

    project_id: Optional[str]
    """Optional project ID.

    If provided, inference uses project context (inherits from user)
    """

    question: Optional[str]
    """User's question or prompt (optional if audio provided)"""

    seed: Optional[int]
    """Base seed for reproducible image generation.

    If not provided, a random seed is used. Only used when output_type='image'
    """

    session_id: Optional[str]
    """Optional session identifier for conversation context"""

    speed: float
    """Speed of the speech (0.25 to 4.0). Only used when audio_type='tts'"""

    use_reasoning: bool
    """
    Use creative reasoning loop for constraint-satisfying generation (only for
    creative_design projects with output_type='image')
    """

    video_base64: Optional[str]
    """Base64 encoded video content"""

    voice: str
    """Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer).

    Only used when audio_type='tts'
    """
