# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = ["ProjectCreateParams"]


class ProjectCreateParams(TypedDict, total=False):
    name: Required[str]
    """Project name"""

    description: Optional[str]
    """Optional project description"""

    project_type: Optional[Literal["creative_design", "general"]]
    """Optional project type override.

    When set, skips LLM classification during content ingestion. Use
    'creative_design' for artistic/design projects, 'general' for
    documentation/business content.
    """

    user_id: Optional[str]
    """User ID to associate the project with.

    If not provided, uses the authenticated user's ID.
    """
