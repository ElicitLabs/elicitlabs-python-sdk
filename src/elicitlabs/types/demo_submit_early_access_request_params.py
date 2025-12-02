# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["DemoSubmitEarlyAccessRequestParams"]


class DemoSubmitEarlyAccessRequestParams(TypedDict, total=False):
    email: Required[str]
    """User's email address"""

    name: Required[str]
    """User's full name"""

    company_size: Optional[str]
    """Company size range"""

    industry: Optional[str]
    """User's industry"""

    role: Optional[str]
    """User's role/job title"""
