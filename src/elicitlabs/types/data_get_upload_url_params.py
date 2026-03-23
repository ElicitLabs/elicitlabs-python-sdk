# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DataGetUploadURLParams"]


class DataGetUploadURLParams(TypedDict, total=False):
    user_id: Required[str]
    """User ID (always required)"""

    callback_url: Optional[str]
    """Optional URL the server will POST to when the job reaches a terminal state."""

    content_description: Optional[str]
    """Optional description of the content being ingested"""

    content_type: Optional[str]
    """Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.

    If omitted, the category is auto-detected after the file is uploaded.
    """

    filename: Optional[str]
    """Filename of the file to upload"""

    notification_email: Optional[str]
    """Optional email address to notify when the job reaches a terminal state."""

    persona_id: Optional[str]
    """Optional persona ID. If provided, data is ingested to this persona"""

    project_id: Optional[str]
    """Optional project ID. If provided, data is ingested to this project"""

    session_id: Optional[str]
    """Session ID for grouping related ingested content"""

    timestamp: Optional[str]
    """ISO-8601 timestamp to preserve original data moment"""
