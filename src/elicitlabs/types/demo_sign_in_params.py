# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DemoSignInParams"]


class DemoSignInParams(TypedDict, total=False):
    email: Required[str]
    """User's email address"""

    password: Required[str]
    """User's password"""
