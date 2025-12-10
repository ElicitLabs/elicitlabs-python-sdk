# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["DemoRetrieveCurrentUserResponse"]


class DemoRetrieveCurrentUserResponse(BaseModel):
    """Response model for user information"""

    created_at: datetime

    email: str

    name: Optional[str] = None

    org_id: Optional[str] = None

    org_name: Optional[str] = None

    user_id: str
