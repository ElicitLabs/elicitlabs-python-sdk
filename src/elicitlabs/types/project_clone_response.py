# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["ProjectCloneResponse", "Project"]


class Project(BaseModel):
    """The newly cloned project"""

    created_at: datetime

    description: Optional[str] = None

    name: str

    project_id: str

    updated_at: Optional[datetime] = None

    user_email: Optional[str] = None

    user_id: str

    user_name: Optional[str] = None

    project_type: Optional[str] = None
    """Project type override: 'creative_design' or 'general'.

    When set, skips LLM classification.
    """


class ProjectCloneResponse(BaseModel):
    """Response model for cloning a project"""

    job_id: str
    """Job ID for tracking the clone operation status via /v1/data/job/status"""

    message: str
    """Success message"""

    project: Project
    """The newly cloned project"""

    source_project_id: str
    """ID of the original project that was cloned"""

    job_id: Optional[str] = None
    """Job ID for tracking async clone operations"""
