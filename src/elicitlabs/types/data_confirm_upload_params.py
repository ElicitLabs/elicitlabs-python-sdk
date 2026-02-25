from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DataConfirmUploadParams"]


class DataConfirmUploadParams(TypedDict, total=False):
    job_id: Required[str]
    """Job ID returned from the upload-url request"""

    object_key: Required[str]
    """Object key returned from the upload-url request"""

    user_id: Required[str]
    """User ID (always required)"""

    content_type: Optional[str]
    """MIME type of the uploaded file"""

    project_id: Optional[str]
    """Optional project ID. If provided, data is ingested to this project"""

    persona_id: Optional[str]
    """Optional persona ID. If provided, data is ingested to this persona"""
