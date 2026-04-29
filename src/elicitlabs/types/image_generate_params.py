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

    aspect_ratio: str
    """Aspect ratio for the generated image, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'."""

    async_mode: bool
    """If true, return a job_id immediately and process in the background"""

    audio_base64: Optional[str]
    """Base64 encoded reference audio for context"""

    callback_url: Optional[str]
    """Optional URL the server will POST to when generation completes."""

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    image_base64: Optional[str]
    """Base64 encoded reference image for context"""

    mask_base64: Optional[str]
    """Optional base64 PNG mask for inpainting (only honored on gpt-image-\\** models).

    Transparent pixels = edit region, opaque pixels = keep. Silently ignored by
    Flux/Imagen/Gemini providers.
    """

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    mode: Optional[Literal["fast", "default", "faithful", "style_transfer", "create_new", "edit"]]
    """
    Generation mode controlling speed vs quality tradeoff and how reference images
    are used. None or 'default': Standard pipeline with memory retrieval and
    context. 'fast': Skip memory retrieval entirely, prompt goes straight to model.
    Fastest. 'faithful': Exact visual reproduction of reference images (entity
    features, colors, proportions). 'style_transfer': Creative adaptation — captures
    entity identity but with creative latitude. 'create_new': Full creative freedom,
    references only inform art style/aesthetic. 'edit': Edit a prior generation
    referenced by source_generation_id; text_input is the feedback / change
    instruction. Skips memory retrieval — the source image IS the context.
    """

    model: str
    """Image generation model ID"""

    notification_email: Optional[str]
    """Optional email address to notify when generation completes."""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    project_id: Optional[str]
    """The project ID"""

    resolution: Literal["1K", "2K", "4K"]
    """Resolution tier for the generated image: '1K', '2K', or '4K'."""

    seed: Optional[int]
    """Random seed for reproducibility"""

    session_id: Optional[str]
    """Session ID for conversation context"""

    source_generation_id: Optional[str]
    """ID of a previously generated image (row in upl.generations) to edit.

    Required when mode='edit'. The server fetches the source from GCS — no upload
    needed. Must belong to the requesting user.
    """

    temperature: Optional[float]
    """Temperature for retrieval LLM calls (0.0-2.0). Lower = more deterministic."""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before generation"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""
