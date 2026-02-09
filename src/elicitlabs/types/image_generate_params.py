# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ImageGenerateParams"]


class ImageGenerateParams(TypedDict, total=False):
    text_input: Required[str]
    """The prompt/description for image generation"""

    user_id: Required[str]
    """The end-user ID"""

    audio_base64: Optional[str]
    """Base64 encoded reference audio for context"""

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    image_base64: Optional[str]
    """Base64 encoded reference image for context"""

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    model: str
    """Image generation model ID"""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    seed: Optional[int]
    """Random seed for reproducibility"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    size: Optional[str]
    """Image dimensions (e.g., 1024x1024)"""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before generation"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""
