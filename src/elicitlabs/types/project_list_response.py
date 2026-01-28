# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

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

    project_type: Optional[str] = None
    """Project type override: 'creative_design' or 'general'.

    When set, skips LLM classification.
    """


class ProjectListResponse(BaseModel):
    """Response model for getting user projects"""

    projects: List[Project]
    """List of projects for the user"""

    total_count: int
    """Total number of projects for the user"""

    user_id: str
    """User ID"""
