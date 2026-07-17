# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ImageGenerateParams", "Consistency", "Edit", "Relayout"]


class ImageGenerateParams(TypedDict, total=False):
    text_input: Required[str]
    """The prompt / change instruction"""

    user_id: Required[str]
    """The end-user ID"""

    aspect_ratio: str
    """Aspect ratio, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'."""

    consistency: Optional[Consistency]
    """Optional explicit visual references for consistency generation."""

    edit: Optional[Edit]
    """Options accepted only when `mode='edit'`."""

    make_editable: Optional[bool]
    """
    When true, intermediate artifacts (raw Gemini base, overlay HTML) are retained
    so the result can be re-edited. Applies to consistency and relayout modes.
    Defaults to true.
    """

    mode: Optional[Literal["default", "consistency", "exploration", "edit", "relayout"]]
    """
    None / 'default' / 'consistency': wireframer → typesetter → synthesizer →
    refiner pipeline that reproduces stored entities/assets faithfully.
    'exploration': creative-freedom path (NOT YET IMPLEMENTED — ships this weekend).
    'edit': edit a prior generation — requires `edit` options. 'relayout': recreate
    a successful-example ad — requires `relayout` options.
    """

    model: str
    """Image generation model ID"""

    project_id: Optional[str]
    """The project ID"""

    relayout: Optional[Relayout]
    """Options accepted only when `mode='relayout'`."""

    resolution: Literal["1K", "2K", "4K"]
    """Resolution tier."""

    seed: Optional[int]
    """Random seed for reproducibility"""


class Consistency(TypedDict, total=False):
    """Optional explicit visual references for consistency generation."""

    reference_ad_ids: SequenceNotStr[str]

    reference_generation_ids: SequenceNotStr[str]


class Edit(TypedDict, total=False):
    """Options accepted only when `mode='edit'`."""

    source_generation_id: Required[str]
    """ID of a previously generated image (row in upl.generations) to edit.

    Server fetches the source from GCS — must belong to the requesting user.
    """


class Relayout(TypedDict, total=False):
    """Options accepted only when `mode='relayout'`."""

    ad_id: Optional[str]
    """The reference AdAsset node_id to recreate."""

    auto_translate_copy: bool
    """When true and locale is set, translate source section copy automatically.

    Explicit copy_overrides take precedence per section.
    """

    copy_overrides: Dict[str, str]
    """Exact per-section copy to typeset for this localized output."""

    locale: Optional[str]
    """Optional BCP-47 locale for this output."""

    output_editability: Literal["standard", "full_editable"]
    """'standard' preserves the existing relayout output.

    'full_editable' adds a design-compatible HTML reproduction, matching
    browser-rendered PNG, and Figma layer manifest after the normal relayout
    completes.
    """

    reuse_base_generation_id: Optional[str]
    """Optional completed relayout generation to reuse as this variant's source."""

    target_aspect_ratios: Optional[SequenceNotStr[str]]
    """List of target aspect ratios (e.g.

    ['1:1', '9:16']). Defaults to ['1:1'] when omitted.
    """
