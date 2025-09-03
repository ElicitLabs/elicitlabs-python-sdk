# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ModalAnalyzeTextParams"]


class ModalAnalyzeTextParams(TypedDict, total=False):
    text_to_analyze: Required[str]
    """The text to analyze for quality improvements"""

    user_id: Required[str]
    """Unique identifier for the user"""

    conversation_history: Optional[Iterable[Dict[str, object]]]
    """Recent conversation messages for context"""

    document_type: str
    """Type of document being analyzed (email/document)"""

    session_id: Optional[str]
    """Session identifier for conversation continuity"""
