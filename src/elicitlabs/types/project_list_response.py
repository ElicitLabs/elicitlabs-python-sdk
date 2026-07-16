# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ProjectListResponse", "Project"]


class Project(BaseModel):
    """Response model for project information"""

    created_at: datetime

    description: Optional[str] = None

    name: str

    project_id: str

    updated_at: Optional[datetime] = None

    user_email: Optional[str] = None

    user_id: str

    user_name: Optional[str] = None

    campaign_id: Optional[str] = None
    """Optional: project belongs to this campaign. Drives co-branded rule fan-out."""

    default_brand_id: Optional[str] = None
    """Optional: used by ingest when an upload omits brand_ids."""

    ingest_autonomy_mode: Optional[Literal["assisted", "autonomous"]] = None
    """Whether uncertain brand/campaign/DAM placement asks for confirmation."""

    project_type: Optional[str] = None
    """Project type override: 'creative_design' or 'general'.

    When set, skips LLM classification.
    """

    use_hierarchical: Optional[bool] = None
    """When True, creative_design projects use hierarchical ingestion.

    When False, uses creative ingest directly.
    """


class ProjectListResponse(BaseModel):
    """Response model for getting user projects"""

    projects: List[Project]
    """List of projects"""

    total_count: int
    """Total number of projects"""

    org_id: Optional[str] = None
    """Organization ID (set when returning org-wide projects)"""

    user_id: Optional[str] = None
    """User ID (set when filtering by user)"""
