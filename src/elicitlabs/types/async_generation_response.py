# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AsyncGenerationResponse"]


class AsyncGenerationResponse(BaseModel):
    """Response returned when a generation is submitted in async mode (HTTP 202)."""

    job_id: Optional[str] = None
    """The job ID to poll for results via client.data.job.retrieve_status()."""

    status: Optional[str] = None
    """Job status, typically "processing"."""

    message: Optional[str] = None
    """Human-readable status message."""
