# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["VideoGenerateResponse"]


class VideoGenerateResponse(BaseModel):
    """Response model for video generation"""

    video_base64: str
    """Base64 encoded video"""

    success: Optional[bool] = None
    """Whether the request succeeded"""
