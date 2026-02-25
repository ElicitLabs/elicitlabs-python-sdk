from typing import Optional

from .._models import BaseModel

__all__ = ["DataConfirmUploadResponse"]


class DataConfirmUploadResponse(BaseModel):
    """Response from confirming an upload"""

    job_id: str
    """Job ID for tracking the processing job"""

    status: str
    """Processing status"""

    message: Optional[str] = None
    """Additional status message"""
