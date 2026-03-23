# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DataConfirmUploadParams"]


class DataConfirmUploadParams(TypedDict, total=False):
    job_id: Required[str]
    """Job ID returned by /ingest/upload-url"""

    object_key: Required[str]
    """GCS object key returned by /ingest/upload-url"""

    user_id: Required[str]
    """User ID (must match the upload-url request)"""

    callback_url: Optional[str]
    """Optional URL the server will POST to when the job reaches a terminal state."""

    content_description: Optional[str]

    content_type: Optional[str]
    """Content category (auto-detected from file bytes if omitted)"""

    filename: Optional[str]

    notification_email: Optional[str]
    """Optional email address to notify when the job reaches a terminal state."""

    persona_id: Optional[str]

    project_id: Optional[str]

    session_id: Optional[str]

    timestamp: Optional[str]
