# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["LinkCreateParams"]


class LinkCreateParams(TypedDict, total=False):
    user_id: Required[str]
    """The user ID to link"""

    callback_url: Optional[str]
    """Optional callback URL to receive a notification when the link is complete."""

    notification_email: Optional[str]
    """Optional email address to receive a notification when the link is complete."""
