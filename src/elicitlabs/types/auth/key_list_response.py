# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["KeyListResponse", "APIKey"]


class APIKey(BaseModel):
    id: str

    created_at: str

    label: Optional[str] = None

    last_used_at: Optional[str] = None

    org_id: str

    user_id: str


class KeyListResponse(BaseModel):
    api_keys: List[APIKey]

    success: Optional[bool] = None
