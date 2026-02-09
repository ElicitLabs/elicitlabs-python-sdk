# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ImageGenerateResponse"]


class ImageGenerateResponse(BaseModel):
    """Response model for image generation"""

    image_base64: str
    """Base64 encoded image"""

    success: Optional[bool] = None
    """Whether the request succeeded"""
