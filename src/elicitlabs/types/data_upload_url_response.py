from .._models import BaseModel

__all__ = ["DataUploadUrlResponse"]


class DataUploadUrlResponse(BaseModel):
    """Response from requesting a signed upload URL"""

    upload_url: str
    """Pre-signed URL for uploading the file via PUT"""

    job_id: str
    """Job ID to use when confirming the upload"""

    object_key: str
    """Cloud storage object key for the uploaded file"""

    expires_in: int
    """Seconds until the upload URL expires"""
