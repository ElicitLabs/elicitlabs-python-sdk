# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["ModalQueryMultimodalityParams"]


class ModalQueryMultimodalityParams(TypedDict, total=False):
    user_id: Required[str]
    """Unique identifier for the user (always required)"""

    audio_base64: Optional[str]
    """Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)"""

    image_base64: Optional[str]
    """Base64 encoded image content"""

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

    video_base64: Optional[str]
    """Base64 encoded video content"""
