# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from datetime import datetime

from .._models import BaseModel

__all__ = ["DemoResetPasswordResponse"]


class DemoResetPasswordResponse(BaseModel):
    message: str
    """Success message"""

    timestamp: datetime
    """When the password was reset"""
