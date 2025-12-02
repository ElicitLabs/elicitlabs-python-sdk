# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DemoRequestPasswordResetResponse"]


class DemoRequestPasswordResetResponse(BaseModel):
    message: str
    """Success message"""
