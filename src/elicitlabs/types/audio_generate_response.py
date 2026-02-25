# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AudioGenerateResponse"]


class AudioGenerateResponse(BaseModel):
    """Response model for audio generation"""

    audio_format: str
    """Audio format (mp3, wav)"""

    audio_type: str
    """Type of audio generated"""

    audio_base64: Optional[str] = None
    """Base64 encoded audio content. Present when the output is under 32 MB."""

    audio_url: Optional[str] = None
    """Signed URL to download the audio.

    Present when the output is 32 MB or larger. Expires after 1 hour.
    """

    duration_seconds: Optional[float] = None
    """Duration of generated audio in seconds"""

    output_type: Optional[str] = None
    """Delivery method for the generated content: 'base64' or 'url'"""

    success: Optional[bool] = None
    """Whether the request succeeded"""
