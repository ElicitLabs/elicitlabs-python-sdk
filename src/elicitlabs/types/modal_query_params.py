# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["ModalQueryParams"]


class ModalQueryParams(TypedDict, total=False):
    user_id: Required[str]
    """Restrict search to this user (required)"""

    audio_base64: Optional[str]
    """Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)"""

    image_base64: Optional[str]
    """Base64 encoded image content"""

    include_modalities: Optional[SequenceNotStr[str]]
    """Filter results by type: ['text', 'image', 'video']"""

    persona_id: Optional[str]
    """Optional persona ID. If provided, query uses persona's context"""

    project_id: Optional[str]
    """Restrict search to this project (required)"""

    session_id: Optional[str]
    """Optional session identifier for conversation context"""

    text_input: Optional[str]
    """Text input to search against.

    The system finds memories _relevant_ to this text.
    """

    video_base64: Optional[str]
    """Base64 encoded video content"""
