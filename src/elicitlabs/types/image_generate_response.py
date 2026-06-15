# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = ["ImageGenerateResponse", "Warning"]


class Warning(BaseModel):
    """Non-blocking warning surfaced to generation clients."""

    code: str
    """Stable warning code."""

    message: str
    """User-facing warning text."""

    details: Optional[Dict[str, object]] = None

    severity: Optional[str] = None
    """warning | info"""


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

    warnings: Optional[List[Warning]] = None
    """Warnings known at queue-accept time.

    Additional generation warnings are returned in the job result and generation
    artifacts after completion.
    """
