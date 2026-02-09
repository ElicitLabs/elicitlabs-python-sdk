# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["ModalQueryResponse"]


class ModalQueryResponse(BaseModel):
    """Unified response model for memory query (text + multimodal)"""

    new_prompt: str
    """Enhanced prompt with retrieved memory context"""

    entity_images: Optional[Dict[str, str]] = None
    """Reference images for matched entities (entity_name -> base64 image)"""

    raw_results: Optional[Dict[str, object]] = None
    """Raw results from the retrieval process"""

    success: Optional[bool] = None
    """Whether the query was processed successfully"""
