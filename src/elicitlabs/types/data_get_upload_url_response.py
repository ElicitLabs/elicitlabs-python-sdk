# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DataGetUploadURLResponse"]


class DataGetUploadURLResponse(BaseModel):
    """Response model for signed upload URL"""

    expires_in: int
    """Seconds until the upload URL expires"""

    job_id: str
    """Job ID to use when confirming the upload"""

    object_key: str
    """GCS object key where the file will live"""

    upload_url: str
    """Signed URL for uploading the file via HTTP PUT"""

    success: Optional[bool] = None
    """Whether the URL was generated"""
