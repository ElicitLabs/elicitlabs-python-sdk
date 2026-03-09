# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["ProjectRetrieveResponse", "Project"]


class Project(BaseModel):
    """The retrieved project"""

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


class ProjectRetrieveResponse(BaseModel):
    """Response model for retrieving a single project (consistent with create/update)"""

    project: Project
    """The retrieved project"""
