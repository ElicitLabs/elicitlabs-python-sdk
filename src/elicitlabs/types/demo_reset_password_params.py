# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DemoResetPasswordParams"]


class DemoResetPasswordParams(TypedDict, total=False):
    token: Required[str]
    """Password reset token"""

    confirm_password: Required[str]
    """Confirmation of new password"""

    new_password: Required[str]
    """New password (minimum 6 characters)"""
