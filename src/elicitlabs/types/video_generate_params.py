# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["VideoGenerateParams"]


class VideoGenerateParams(TypedDict, total=False):
    text_input: Required[str]
    """The prompt/description for video generation"""

    user_id: Required[str]
    """The end-user ID"""

    advanced_creative: bool
    """
    Enable first+last frame workflow: generates a starting frame and an ending frame
    via the image pipeline, then uses Veo's first-and-last-frame feature to animate
    the transition between them.
    """

    aspect_ratio: str
    """Aspect ratio for the generated video: '16:9' or '9:16'."""

    async_mode: bool
    """Run generation asynchronously. When true, returns a job_id instead of the result."""

    audio_base64: Optional[str]
    """Base64 encoded reference audio for context"""

    callback_url: Optional[str]
    """URL to POST results to when async generation completes. Implies async_mode=true."""

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    duration: Optional[float]
    """Target duration in seconds"""

    image_base64: Optional[str]
    """Base64 encoded reference image for context (e.g., start frame)"""

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    model: str
    """Video generation model ID"""

    notification_email: Optional[str]
    """Email address to notify when the job completes."""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    seed: Optional[int]
    """Random seed for reproducibility"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before generation"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""
