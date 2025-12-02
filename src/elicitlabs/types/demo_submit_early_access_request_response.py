# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["DemoSubmitEarlyAccessRequestResponse"]


class DemoSubmitEarlyAccessRequestResponse(BaseModel):
    id: str
    """Submission ID"""

    created_at: datetime
    """Submission timestamp"""

    email: str
    """User's email address"""

    message: str
    """Success message"""

    name: str
    """User's full name"""

    company_size: Optional[str] = None
    """Company size range"""

    industry: Optional[str] = None
    """User's industry"""

    role: Optional[str] = None
    """User's role/job title"""
