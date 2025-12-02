# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["AuthAuthenticateWithGoogleParams"]


class AuthAuthenticateWithGoogleParams(TypedDict, total=False):
    credential: Required[str]
    """JWT token from Google Sign-In"""
