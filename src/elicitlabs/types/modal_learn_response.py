# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ModalLearnResponse"]


class ModalLearnResponse(BaseModel):
    """Response model for learning processing"""

    session_id: str
    """Session identifier used for the learning"""

    success: Optional[bool] = None
    """Whether the learning was processed successfully"""
