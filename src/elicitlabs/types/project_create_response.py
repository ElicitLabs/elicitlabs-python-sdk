# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

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


class ProjectCreateResponse(BaseModel):
    """Response model for creating a project"""

    message: str
    """Success message"""

    project: Project
    """The created project"""
