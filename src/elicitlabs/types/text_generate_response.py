# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TextGenerateResponse"]


class TextGenerateResponse(BaseModel):
    """Response model for text generation"""

    text: str
    """Generated text response"""

    success: Optional[bool] = None
    """Whether the request succeeded"""
