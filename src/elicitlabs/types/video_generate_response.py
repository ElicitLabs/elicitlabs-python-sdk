# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["VideoGenerateResponse"]


class VideoGenerateResponse(BaseModel):
    """Response model for video generation"""

    output_type: Optional[str] = None
    """Delivery method for the generated content: 'base64' or 'url'"""

    success: Optional[bool] = None
    """Whether the request succeeded"""

    video_base64: Optional[str] = None
    """Base64 encoded video. Present when the output is under 32 MB."""

    video_url: Optional[str] = None
    """Signed URL to download the video.

    Present when the output is 32 MB or larger. Expires after 1 hour.
    """
