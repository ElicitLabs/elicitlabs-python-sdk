# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

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

    resolution: Optional[Literal["1K", "2K", "4K"]]
    """Override the resolution tier derived from 'size'.

    Accepted values: '1K', '2K', '4K'. When set, this takes precedence over the
    resolution inferred from the size parameter.
    """

    seed: Optional[int]
    """Random seed for reproducibility"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    size: Optional[str]
    """Image dimensions as WxH, e.g.

    '1024x1024', '1920x1080', '1080x1920'. Automatically converted to the nearest
    supported aspect ratio (1:1, 16:9, 9:16, …) and resolution tier (1K / 2K / 4K).
    """

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before generation"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""
