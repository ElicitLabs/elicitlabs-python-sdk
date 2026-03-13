# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["AudioGenerateResponse"]


class AudioGenerateResponse(BaseModel):
    """Response model for audio generation"""

    audio_format: str
    """Audio format, e.g. mp3, wav"""

    audio_type: str
    """Type of audio generated"""

    audio_base64: Optional[str] = None
    """Base64 encoded audio content.

    Present when the payload is under ~30 MB. May be absent for very large outputs.
    """

    audio_url: Optional[str] = None
    """Signed GCS URL to download the audio (expires after 24 h).

    Always present when the upload succeeds.
    """

    duration_seconds: Optional[float] = None
    """Duration of generated audio in seconds"""

    output_type: Optional[str] = None
    """
    Delivery method: 'both' (base64 + url), 'url' (url only, base64 omitted due to
    size), or 'base64' (GCS upload failed).
    """

    success: Optional[bool] = None
    """Whether the request succeeded"""
