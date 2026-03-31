# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["LinkCreateResponse"]


class LinkCreateResponse(BaseModel):
    """Response model for linking a user to a persona"""

    message: str

    persona_id: str

    user_id: str

    cloned_persona_id: Optional[str] = None

    job_id: Optional[str] = None
    """Job ID for tracking the clone operation status via /v1/data/job/status"""
