# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["JobRetrieveStatusResponse"]


class JobRetrieveStatusResponse(BaseModel):
    """Response model for job completion percentage"""

    job_id: str
    """The job ID"""

    status: str
    """Current job status: done, partial, processing, not started, error"""

    completion: Optional[int] = None
    """Completion percentage (0-100)"""
