# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PersonaListLinkedResponse", "Persona"]


class Persona(BaseModel):
    """Response model for persona information"""

    created_at: datetime

    description: Optional[str] = None

    name: str

    persona_id: str

    user_email: Optional[str] = None

    user_id: str

    user_name: Optional[str] = None


class PersonaListLinkedResponse(BaseModel):
    """Response for listing personas linked to a user"""

    personas: List[Persona]

    total_count: int

    user_id: str
