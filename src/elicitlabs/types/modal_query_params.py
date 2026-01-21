# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ModalQueryParams"]


class ModalQueryParams(TypedDict, total=False):
    question: Required[str]
    """The question to query against user's memories"""

    user_id: Required[str]
    """Unique identifier for the user (always required)"""

    filter_memory_types: Optional[SequenceNotStr[str]]
    """Optional list of memory types to exclude from retrieval.

    Valid types: 'episodic', 'preference', 'identity', 'short_term'
    """

    persona_id: Optional[str]
    """Optional persona ID.

    If provided, query is scoped to this persona instead of the user
    """

    project_id: Optional[str]
    """Optional project ID.

    If provided, query is scoped to this project (inherits from user)
    """

    session_id: Optional[str]
    """Optional session identifier for conversation context"""
