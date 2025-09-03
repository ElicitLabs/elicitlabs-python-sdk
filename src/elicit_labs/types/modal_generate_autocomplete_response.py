# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ModalGenerateAutocompleteResponse"]


class ModalGenerateAutocompleteResponse(BaseModel):
    action: str
    """Action to take: 'complete' or 'wait'"""

    confidence: float
    """Confidence score (0.0-1.0)"""

    processing_time_seconds: float
    """Time taken to process"""

    cache_hit: Optional[bool] = None
    """Whether result came from cache"""

    completion: Optional[str] = None
    """Text completion if action is 'complete'"""

    success: Optional[bool] = None
    """Whether the request was successful"""
