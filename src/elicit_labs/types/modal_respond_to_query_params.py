# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ModalRespondToQueryParams"]


class ModalRespondToQueryParams(TypedDict, total=False):
    message: Required[str]
    """Single message string to process"""

    session_id: Required[str]
    """Session identifier for conversation continuity"""

    user_id: Required[str]
    """Unique identifier for the user"""
