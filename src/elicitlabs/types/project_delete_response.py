# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["ProjectDeleteResponse"]


class ProjectDeleteResponse(BaseModel):
    """Response model for deleting a project"""

    message: str
    """Success message"""

    project_id: str
    """ID of deleted project"""
