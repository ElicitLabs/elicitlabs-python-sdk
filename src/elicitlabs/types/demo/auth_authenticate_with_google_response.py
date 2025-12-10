# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ..._models import BaseModel

__all__ = ["AuthAuthenticateWithGoogleResponse"]


class AuthAuthenticateWithGoogleResponse(BaseModel):
    """Response model for authentication"""

    access_token: str
    """JWT access token"""

    expires_in: int
    """Token expiration time in seconds"""

    user: Dict[str, object]
    """User information"""

    token_type: Optional[str] = None
    """Token type"""
