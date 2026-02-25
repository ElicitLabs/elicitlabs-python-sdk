from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DataUploadUrlParams"]


class DataUploadUrlParams(TypedDict, total=False):
    user_id: Required[str]
    """User ID (always required)"""

    filename: Required[str]
    """Original filename of the file to upload"""

    content_type: Optional[str]
    """MIME type of the file (auto-detected if omitted)"""

    project_id: Optional[str]
    """Optional project ID. If provided, data is ingested to this project"""

    persona_id: Optional[str]
    """Optional persona ID. If provided, data is ingested to this persona"""
