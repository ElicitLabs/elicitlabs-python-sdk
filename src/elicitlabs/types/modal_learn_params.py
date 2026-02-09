# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ModalLearnParams", "Message"]


class ModalLearnParams(TypedDict, total=False):
    messages: Required[Iterable[Message]]
    """A standard chat history list. Can contain Text, Image, Video, and Audio."""

    user_id: Required[str]
    """The user these memories belong to (required)"""

    persona_id: Optional[str]
    """Optional persona ID. Link these memories to a specific persona."""

    project_id: Optional[str]
    """The project bucket (optional)"""

    session_id: Optional[str]
    """Optional session identifier for conversation context"""

    timestamp: Optional[str]
    """ISO format datetime string for the message timestamp"""


class Message(TypedDict, total=False):
    """A single message in the learning context"""

    content: Required[str]
    """Message content or Link"""

    role: Optional[str]
    """Message role: 'user', 'assistant', or 'system'"""

    type: Optional[str]
    """Content type for multimodal: 'text', 'image', 'video', 'audio'"""
