# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["LinkDeleteResponse"]


class LinkDeleteResponse(BaseModel):
    """Response model for linking a user to a persona"""

    message: str

    persona_id: str

    user_id: str

    cloned_persona_id: Optional[str] = None
