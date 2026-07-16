# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ProjectCreateResponse", "Project"]


class Project(BaseModel):
    """The created project"""

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


class ProjectCreateResponse(BaseModel):
    """Response model for creating a project"""

    message: str
    """Success message"""

    project: Project
    """The created project"""
