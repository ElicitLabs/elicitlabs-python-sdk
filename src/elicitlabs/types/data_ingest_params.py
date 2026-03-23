# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["DataIngestParams"]


class DataIngestParams(TypedDict, total=False):
    payload: Required[Union[str, Dict[str, object], Iterable[object]]]
    """Raw content as string, object, list (for messages), or base64 encoded data"""

    user_id: Required[str]
    """User ID (always required)"""

    callback_url: Optional[str]
    """
    Optional URL the server will POST to when the job reaches a terminal state
    (done, error, cancelled). The payload will match the /v1/data/job/status
    response shape.
    """

    content_description: Optional[str]
    """
    Optional description of the content being ingested (e.g., 'Logo design
    concepts', 'Meeting notes')
    """

    content_type: Optional[str]
    """Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.

    If omitted, the category is auto-detected from the uploaded file bytes.
    """

    filename: Optional[str]
    """Filename of the uploaded file"""

    notification_email: Optional[str]
    """Optional email address to notify when the job reaches a terminal state."""

    persona_id: Optional[str]
    """Optional persona ID.

    If provided, data is ingested to this persona instead of the user
    """

    project_id: Optional[str]
    """Optional project ID.

    If provided, data is ingested to this project (inherits from user)
    """

    session_id: Optional[str]
    """
    Session ID for grouping related ingested content and enabling session-based
    retrieval
    """

    timestamp: Optional[str]
    """ISO-8601 timestamp to preserve original data moment"""
