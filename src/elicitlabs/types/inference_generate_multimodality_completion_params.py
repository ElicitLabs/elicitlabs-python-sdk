# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["InferenceGenerateMultimodalityCompletionParams"]


class InferenceGenerateMultimodalityCompletionParams(TypedDict, total=False):
    user_id: Required[str]
    """Unique identifier for the user"""

    audio_base64: Optional[str]
    """Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)"""

    context: Optional[str]
    """Additional context for the question"""

    disabled_learning: bool
    """Whether to disable learning/ingestion of the multimodal content"""

    image_base64: Optional[str]
    """Base64 encoded image content"""

    model: Optional[str]
    """LLM model to use for generating the response"""

    output_type: Literal["text", "audio", "image"]
    """
    Output type: 'text' for text only, 'audio' for TTS audio, 'image' for
    AI-generated image
    """

    question: Optional[str]
    """User's question or prompt (optional if audio provided)"""

    session_id: Optional[str]
    """Optional session identifier for conversation context"""

    speed: float
    """Speed of the speech (0.25 to 4.0)"""

    video_base64: Optional[str]
    """Base64 encoded video content"""

    voice: str
    """Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer)"""
