# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AppContext"]


class AppContext(BaseModel):
    app_name: str
    """Name of the application"""

    app_type: Optional[str] = None
    """Type of application (e.g., email_client)"""

    app_version: Optional[str] = None
    """Version of the application"""
