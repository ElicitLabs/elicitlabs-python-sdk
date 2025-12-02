# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DemoCreateUserParams"]


class DemoCreateUserParams(TypedDict, total=False):
    email: Required[str]
    """User's email address"""

    name: Required[str]
    """User's full name"""

    password: Required[str]
    """User's password (minimum 6 characters)"""

    org_id: Optional[str]
    """Optional organization ID.

    If not provided, a default organization will be created automatically with the
    format 'Org: {user_name}'
    """
