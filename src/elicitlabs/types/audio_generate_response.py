# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AudioGenerateResponse"]


class AudioGenerateResponse(BaseModel):
    """Response model for audio generation"""

    audio_base64: str
    """Base64 encoded audio content"""

    audio_format: str
    """Audio format (mp3, wav)"""

    audio_type: str
    """Type of audio generated"""

    duration_seconds: Optional[float] = None
    """Duration of generated audio in seconds"""

    success: Optional[bool] = None
    """Whether the request succeeded"""
