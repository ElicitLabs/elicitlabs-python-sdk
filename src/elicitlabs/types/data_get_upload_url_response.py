# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DataGetUploadURLResponse"]


class DataGetUploadURLResponse(BaseModel):
<<<<<<< HEAD
    """Response from requesting a signed upload URL"""

    upload_url: str
    """Pre-signed URL for uploading the file via PUT"""
=======
    """Response model for signed upload URL"""

    expires_in: int
    """Seconds until the upload URL expires"""
>>>>>>> b4627a799871d5ab98a875b7d62e0ed217cd539b

    job_id: str
    """Job ID to use when confirming the upload"""

    object_key: str
<<<<<<< HEAD
    """Cloud storage object key for the uploaded file"""

    expires_in: int
    """Seconds until the upload URL expires"""
=======
    """GCS object key where the file will live"""

    upload_url: str
    """Signed URL for uploading the file via HTTP PUT"""

    success: Optional[bool] = None
    """Whether the URL was generated"""
>>>>>>> b4627a799871d5ab98a875b7d62e0ed217cd539b
