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

    aspect_ratio: str
    """Aspect ratio for the generated image, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'."""

    async_mode: bool
    """If true, return a job_id immediately and process in the background"""

    audio_base64: Optional[str]
    """Base64 encoded reference audio for context"""

    callback_url: Optional[str]
    """Optional URL the server will POST to when generation completes."""

    debug: bool
    """
    If true, capture a self-contained HTML trace of every pipeline step (retrieval
    LLM calls, synthesis, prompt assembly, image LLM, post-gen text fix, edit-text
    refinement loop) to data/temp/<ts>\\__pipeline_trace.html. Also activates
    automatically when the server is started with the `DEBUG` environment variable
    set to a truthy value (true/1/yes).
    """

    disabled_learning: bool
    """If true, this request is ignored by long-term memory"""

    fan_out_group_id: Optional[str]
    """
    Frontend-generated UUID shared across the 3 parallel generations the playground
    fires per fan-out (one per text_strategy). Persisted on every generation row so
    the client can re-group siblings after page refresh. Send the SAME value on all
    3 of the calls in one comparison; omit (null) for non-fan-out generations.
    """

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

    mask_base64: Optional[str]
    """Optional base64 PNG mask for inpainting (only honored on gpt-image-\\** models).

    Transparent pixels = edit region, opaque pixels = keep. Silently ignored by
    Flux/Imagen/Gemini providers.
    """

    max_reasoning_iterations: int
    """Max reasoning steps if reasoning is enabled"""

    mode: Optional[Literal["fast", "default", "consistency", "exploration", "edit"]]
    """Generation mode controlling how reference assets are used.

    None or 'default': Standard pipeline — synthesis LLM picks consistency vs
    exploration based on the prompt. 'consistency': Reproduce stored entities/assets
    faithfully — match their canonical look and the project's documented details.
    'exploration': Creative freedom — generate new content / new compositions where
    references guide aesthetic and style only, not exact appearance. The post-gen
    text fix is skipped in this mode (the model's own text rendering is trusted).
    'fast': Skip hierarchical retrieval, single-call block selector. 'edit': Edit a
    prior generation referenced by source_generation_id; text_input is the change
    instruction. Skips memory retrieval — the source image IS the context. Legacy
    values 'faithful', 'style_transfer', 'create_new' are auto-coerced
    ('faithful'→'consistency', the other two→'exploration').
    """

    model: str
    """Image generation model ID"""

    notification_email: Optional[str]
    """Optional email address to notify when generation completes."""

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

    temperature: Optional[float]
    """Temperature for retrieval LLM calls (0.0-2.0). Lower = more deterministic."""

    text_strategy: Optional[Literal["overlay", "single_gemini", "baked"]]
    """Typography strategy for mode='consistency'.

    'overlay' (default): HTML text-overlay rendered by Playwright and
    alpha-composited on top of Gemini's no-text render, with a Claude refinement
    loop. Best typography fidelity. 'single_gemini': one Gemini call generates the
    full image (text included) using the consistency-flavored prompt — fast and
    cheap, but Gemini may hallucinate fonts. 'baked': Claude synthesizes the
    typography reference, then Gemini paints that text into the final pixels in one
    call — best balance of typography fidelity and scene integration. Ignored when
    mode is not 'consistency'.
    """

    use_reasoning: bool
    """Enable Chain-of-Thought/Reasoning steps before generation"""

    video_base64: Optional[str]
    """Base64 encoded reference video for context"""
