# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["ProjectCreateParams"]


class ProjectCreateParams(TypedDict, total=False):
    name: Required[str]
    """Project name"""

    campaign_id: Optional[str]
    """Optional: campaign this project belongs to (drives co-branded rule fan-out)."""

    default_brand_id: Optional[str]
    """Optional: brand used by ingest when an upload omits brand_ids."""

    description: Optional[str]
    """Optional project description"""

    project_type: Literal["creative_design", "general"]
    """Project type override.

    When set, skips LLM classification during content ingestion. Use
    'creative_design' for artistic/design projects, 'general' for
    documentation/business content.
    """

    use_hierarchical: bool
    """
    When True (default), creative_design projects use the hierarchical ingestion
    pipeline. Set to False to skip hierarchical and go directly to creative ingest.
    """

    user_id: Optional[str]
    """User ID to associate the project with.

    If not provided, uses the authenticated user's ID.
    """

    x_organization_id: Annotated[str, PropertyInfo(alias="X-Organization-ID")]
