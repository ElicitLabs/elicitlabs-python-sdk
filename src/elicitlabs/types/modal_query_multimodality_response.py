# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["ModalQueryMultimodalityResponse"]


class ModalQueryMultimodalityResponse(BaseModel):
    """Response model for multimodal memory query"""

    new_prompt: str
    """Formatted string containing retrieved memories"""

    entity_images: Optional[Dict[str, str]] = None
    """Reference images for matched entities (entity_name -> base64 image)"""

    image_base64: Optional[str] = None
    """
    Base64 encoded image - either the original image or a representative frame from
    video
    """

    raw_results: Optional[Dict[str, object]] = None
    """Raw results from the memory retrieval"""

    success: Optional[bool] = None
    """Whether the query was processed successfully"""
