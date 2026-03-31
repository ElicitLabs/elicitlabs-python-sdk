# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["JobRetrieveStatusResponse"]


class JobRetrieveStatusResponse(BaseModel):
    """Response model for job completion percentage"""

    job_id: str
    """The job ID"""

    status: str
    """Current job status: done, partial, processing, not started, error, cancelled"""

    completion: Optional[int] = None
    """Completion percentage (0-100)"""

    error_details: Optional[str] = None
    """Error details (available when status is 'error')"""

    job_type: Optional[str] = None
    """Type of job (e.g. 'ingest', 'clone_project', 'generation_image')"""

    result: Optional[Dict[str, object]] = None
    """Job result data (available when status is 'done')"""
