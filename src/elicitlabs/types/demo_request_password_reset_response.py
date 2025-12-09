# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DemoRequestPasswordResetResponse"]


class DemoRequestPasswordResetResponse(BaseModel):
    """Response model for forgot password"""

    message: str
    """Success message"""
