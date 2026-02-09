# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DataIngestResponse"]


class DataIngestResponse(BaseModel):
    """Response model for data ingestion"""

    job_id: str
    """Unique job identifier for tracking"""

    status: str
    """Processing status ('accepted', 'queued', 'failed')"""

    message: Optional[str] = None
    """Additional status or error message"""

    success: Optional[bool] = None
    """Whether the request was accepted successfully"""
