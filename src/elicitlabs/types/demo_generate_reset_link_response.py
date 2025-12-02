# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DemoGenerateResetLinkResponse"]


class DemoGenerateResetLinkResponse(BaseModel):
    token: str
    """Reset token"""

    expires_in: int
    """Token expiration time in seconds"""

    reset_url: str
    """Password reset URL"""
