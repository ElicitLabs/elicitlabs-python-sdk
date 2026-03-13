# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["VideoGenerateResponse"]


class VideoGenerateResponse(BaseModel):
    """Response model for video generation"""

    output_type: Optional[str] = None
    """
    Delivery method: 'both' (base64 + url), 'url' (url only, base64 omitted due to
    size), or 'base64' (GCS upload failed).
    """

    success: Optional[bool] = None
    """Whether the request succeeded"""

    video_base64: Optional[str] = None
    """Base64 encoded video.

    Present when the payload is under ~30 MB. May be absent for very large outputs.
    """

    video_format: Optional[str] = None
    """Video format, e.g. mp4, webm"""

    video_url: Optional[str] = None
    """Signed GCS URL to download the video (expires after 24 h).

    Always present when the upload succeeds.
    """
