# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .app_context_param import AppContextParam

__all__ = ["ModalInitializeParams"]


class ModalInitializeParams(TypedDict, total=False):
    app_context: Required[AppContextParam]
    """Application context information"""

    session_id: Required[str]
    """Session identifier for conversation continuity"""

    user_id: Required[str]
    """Unique identifier for the user"""

    screenshot_base64: Optional[str]
    """Base64 encoded screenshot for analysis"""

    screenshot_path: Optional[str]
    """Path to screenshot file for analysis"""
