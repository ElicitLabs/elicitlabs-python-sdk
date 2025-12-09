# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime

from ..._models import BaseModel

__all__ = ["OrgListOrganizationMembersResponse", "User"]


class User(BaseModel):
    """Response model for organization member (user or persona)"""

    id: str
    """User ID or Persona ID"""

    created_at: datetime
    """Creation timestamp"""

    type: str
    """Type: 'user' or 'persona'"""

    description: Optional[str] = None
    """Description (for personas only)"""

    email: Optional[str] = None
    """Email (for users only)"""

    name: Optional[str] = None
    """Name of user or persona"""

    org_id: Optional[str] = None
    """Organization ID (for users only)"""

    org_name: Optional[str] = None
    """Organization name (for users only)"""

    user_id: Optional[str] = None
    """Owner user ID (for personas only)"""


class OrgListOrganizationMembersResponse(BaseModel):
    """Response model for getting users and personas by organization"""

    org_id: str
    """Organization ID"""

    total_count: int
    """Total number of users and personas in the organization"""

    users: List[User]
    """List of users and personas in the organization"""
