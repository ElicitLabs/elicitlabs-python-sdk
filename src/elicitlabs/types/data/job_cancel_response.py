# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["JobCancelResponse"]


class JobCancelResponse(BaseModel):
    """Response model for job cancellation"""

    cancelled_count: int
    """Number of jobs cancelled (including descendants)"""

    job_id: str
    """The root job ID that was cancelled"""

    status: str
    """Result status: 'cancelled' or 'already_terminal'"""
