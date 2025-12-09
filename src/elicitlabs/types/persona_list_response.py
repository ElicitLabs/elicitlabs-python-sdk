# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from .._models import BaseModel

__all__ = ["PersonaListResponse", "Persona"]


class Persona(BaseModel):
    """Response model for persona information"""

    created_at: datetime

    description: Optional[str] = None

    name: str

    persona_id: str

    user_email: Optional[str] = None

    user_id: str

    user_name: Optional[str] = None


class PersonaListResponse(BaseModel):
    """Response model for getting user personas"""

    personas: List[Persona]
    """List of personas for the user"""

    total_count: int
    """Total number of personas for the user"""

    user_id: str
    """User ID"""
