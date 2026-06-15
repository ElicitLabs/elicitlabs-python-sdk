# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["KeyCreateResponse"]


class KeyCreateResponse(BaseModel):
    id: str

    api_key: str

    created_at: str

    label: Optional[str] = None

    org_id: str

    user_id: str

    success: Optional[bool] = None
