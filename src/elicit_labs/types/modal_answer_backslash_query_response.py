# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ModalAnswerBackslashQueryResponse"]


class ModalAnswerBackslashQueryResponse(BaseModel):
    confidence: float
    """Confidence score (0.0-1.0)"""

    processing_time_seconds: float
    """Time taken to process"""

    reasoning: str
    """Brief explanation of why this answer fits or why null was returned"""

    answer: Optional[str] = None
    """
    The answer that fits perfectly in the context, or null if insufficient
    information
    """

    memory_retrieval_used: Optional[bool] = None
    """Whether memory retrieval was used"""

    success: Optional[bool] = None
    """Whether the request was successful"""
