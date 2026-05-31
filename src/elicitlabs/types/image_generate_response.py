# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ImageGenerateResponse"]


class ImageGenerateResponse(BaseModel):
    """Returned when an image generation job has been enqueued."""

    generation_id: str
    """Persisted upl.generations row ID for this image"""

    job_id: str
    """Job ID for /v1/data/job/status polling"""

    message: Optional[str] = None
    """Polling guidance for the caller"""

    status: Optional[str] = None
    """Initial queued status"""
