# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ModalAnswerBackslashQueryParams"]


class ModalAnswerBackslashQueryParams(TypedDict, total=False):
    context_text: Required[str]
    """The surrounding text context where the answer should fit"""

    query: Required[str]
    """The query/question to answer within the context"""

    user_id: Required[str]
    """Unique identifier for the user"""

    conversation_history: Optional[Iterable[Dict[str, object]]]
    """Recent conversation messages for context"""

    document_type: str
    """Type of document (email/document)"""

    session_id: Optional[str]
    """Session identifier for conversation continuity"""
