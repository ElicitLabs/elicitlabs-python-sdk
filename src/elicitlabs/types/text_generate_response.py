# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["TextGenerateResponse"]


class TextGenerateResponse(BaseModel):
    """Response model for text generation"""

    structured_output: Optional[Dict[str, object]] = None
    """
    Structured JSON output matching the requested output_schema (when output_schema
    is provided)
    """

    success: Optional[bool] = None
    """Whether the request succeeded"""

    text: Optional[str] = None
    """Generated text response (when no output_schema is provided)"""
