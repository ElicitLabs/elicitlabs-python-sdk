# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PersonaRetrieveResponse", "Persona"]


class Persona(BaseModel):
    """The retrieved persona"""

    created_at: datetime

    description: Optional[str] = None

    name: str

    persona_id: str

    user_email: Optional[str] = None

    user_id: str

    user_name: Optional[str] = None


class PersonaRetrieveResponse(BaseModel):
    """Response model for retrieving a single persona (consistent with create/update)"""

    persona: Persona
    """The retrieved persona"""
