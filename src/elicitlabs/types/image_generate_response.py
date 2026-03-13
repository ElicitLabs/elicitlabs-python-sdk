# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ImageGenerateResponse"]


class ImageGenerateResponse(BaseModel):
    """Response model for image generation"""

    image_base64: Optional[str] = None
    """Base64 encoded image.

    Present when the payload is under ~30 MB. May be absent for very large outputs.
    """

    image_format: Optional[str] = None
    """Image format, e.g. png, jpeg, webp"""

    image_url: Optional[str] = None
    """Signed GCS URL to download the image (expires after 24 h).

    Always present when the upload succeeds.
    """

    output_type: Optional[str] = None
    """
    Delivery method: 'both' (base64 + url), 'url' (url only, base64 omitted due to
    size), or 'base64' (GCS upload failed).
    """

    success: Optional[bool] = None
    """Whether the request succeeded"""
