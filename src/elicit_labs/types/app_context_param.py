# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["AppContextParam"]


class AppContextParam(TypedDict, total=False):
    app_name: Required[str]
    """Name of the application"""

    app_type: Optional[str]
    """Type of application (e.g., email_client)"""

    app_version: Optional[str]
    """Version of the application"""
