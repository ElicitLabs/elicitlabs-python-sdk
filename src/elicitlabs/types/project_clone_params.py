# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ProjectCloneParams"]


class ProjectCloneParams(TypedDict, total=False):
    project_id: Required[str]
    """ID of the project to clone"""

    description: Optional[str]
    """Description for the cloned project. Defaults to the original's description."""

    name: Optional[str]
    """Name for the cloned project. Defaults to '{original_name} (Copy)'."""

    source_user_id: str
    """User ID of the source project owner.

    If not provided, uses the authenticated user's ID.
    """

    target_user_id: Optional[str]
    """Target user ID to own the cloned project.

    If not provided, uses the authenticated user.
    """
