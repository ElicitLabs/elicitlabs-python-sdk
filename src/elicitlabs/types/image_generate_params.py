# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ImageGenerateParams", "Edit", "Relayout"]


class ImageGenerateParams(TypedDict, total=False):
    text_input: Required[str]
    """The prompt / change instruction"""

    user_id: Required[str]
    """The end-user ID"""

    aspect_ratio: str
    """Aspect ratio, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'."""

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


class Edit(TypedDict, total=False):
    """Options accepted only when `mode='edit'`."""

    source_generation_id: Required[str]
    """ID of a previously generated image (row in upl.generations) to edit.

    Server fetches the source from GCS — must belong to the requesting user.
    """


class Relayout(TypedDict, total=False):
    """Options accepted only when `mode='relayout'`."""

    ad_id: Required[str]
    """The reference AdAsset node_id to recreate."""

    target_aspect_ratios: Optional[SequenceNotStr[str]]
    """List of target aspect ratios (e.g.

    ['1:1', '9:16']). Defaults to ['1:1'] when omitted.
    """
