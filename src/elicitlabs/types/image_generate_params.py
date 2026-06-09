# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ImageGenerateParams"]


class ImageGenerateParams(TypedDict, total=False):
    text_input: Required[str]
    """The prompt/description for image generation"""

    user_id: Required[str]
    """The end-user ID"""

    ad_id: Optional[str]
    """Relayout mode only: the reference ad's ObjectNode node_id to recreate.

    Either this OR `auto_select_ad` must be set.
    """

    aspect_ratio: str
    """Aspect ratio for the generated image, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'."""

    audio_base64: Optional[str]
    """Base64 encoded reference audio for context"""

    auto_select_ad: bool
    """
    Relayout mode only: when true and `ad_id` is null, a VLM judge picks the best
    analyzed ad from the project.
    """

    debug: bool
    """Deprecated no-op. Generation pipeline HTML tracing has been removed."""

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    font_reference_image_base64: Optional[SequenceNotStr[str]]
    """
    List of base64-encoded PNG/JPG images showing the desired font (e.g., a
    typography specimen). Honored only when mode='edit'.
    """

    font_reference_image_url: Optional[SequenceNotStr[str]]
    """List of HTTPS or gs:// URLs to images showing the desired font.

    Server downloads them. Honored only when mode='edit'.
    """

    font_reference_ttf_base64: Optional[SequenceNotStr[str]]
    """
    List of base64-encoded TTF/OTF font file bytes (drag-and-drop support — no
    upload endpoint required). The server decodes, renders a typography sample, and
    passes the rendered image as a reference. Honored only when mode='edit'.
    """

    font_reference_ttf_url: Optional[SequenceNotStr[str]]
    """List of HTTPS or gs:// URLs to TTF/OTF font files.

    The server renders a typography sample in each font and passes the rendered
    image as a reference. Honored only when mode='edit'.
    """

    image_base64: Optional[str]
    """Base64 encoded reference image for context"""

    make_editable: Optional[bool]
    """
    When true, the response includes `gemini_base_url` — the raw Gemini recreation
    before any text overlay is composited. Applies to relayout and consistency
    modes. When false or omitted, only the final output is returned.
    """

    mask_base64: Optional[str]
    """Optional base64 PNG mask for inpainting (only honored on gpt-image-\\** models).

    Transparent pixels = edit region, opaque pixels = keep. Silently ignored by
    Flux/Imagen/Gemini providers.
    """

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    mode: Optional[Literal["fast", "default", "consistency", "exploration", "edit", "relayout"]]
    """Generation mode controlling how reference assets are used.

    None or 'default': Standard pipeline — synthesis LLM picks consistency vs
    exploration based on the prompt. 'consistency': Reproduce stored entities/assets
    faithfully — match their canonical look and the project's documented details.
    'exploration': Creative freedom — generate new content / new compositions where
    references guide aesthetic and style only, not exact appearance. The post-gen
    text fix is skipped in this mode (the model's own text rendering is trusted).
    'fast': Skip hierarchical retrieval, single-call block selector. 'edit': Edit a
    prior generation referenced by source_generation_id; text_input is the change
    instruction. Skips memory retrieval — the source image IS the context.
    'relayout': Recreate a successful-example ad through the full wireframer →
    typesetter → synthesizer → refiner pipeline using the LayoutAnalysis ingested
    for the chosen ad. Provide `ad_id` or set `auto_select_ad=true` to let a VLM
    pick the best ad from the project. Per-stage progress lands in
    `metadata.relayout_steps` for FE polling. Legacy values 'faithful',
    'style_transfer', 'create_new' are auto-coerced ('faithful'→'consistency', the
    other two→'exploration').
    """

    model: str
    """Image generation model ID"""

    persona_id: Optional[str]
    """The specific system persona/voice to use"""

    pinned_entity_ids: Optional[SequenceNotStr[str]]
    """OBJECTS entity node IDs to anchor flat memory retrieval.

    When set, memory retrieval focuses on episodes/memories connected to these
    specific entities instead of fully autonomous semantic search.
    """

    pinned_folder_ids: Optional[SequenceNotStr[str]]
    """HierarchicalFolder node IDs to anchor hierarchical retrieval.

    When set, the retrieval pipeline targets these folders directly instead of using
    LLM path selection.
    """

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

    target_aspect_ratios: Optional[SequenceNotStr[str]]
    """Relayout mode only: comma-separable list of target aspect ratios (e.g.

    ['1:1', '9:16']). Defaults to ['1:1'] when omitted.
    """

    temperature: Optional[float]
    """Temperature for retrieval LLM calls (0.0-2.0). Lower = more deterministic."""

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before generation"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""
