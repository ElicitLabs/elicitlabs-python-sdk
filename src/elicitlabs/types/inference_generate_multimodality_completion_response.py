# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .._models import BaseModel

__all__ = ["InferenceGenerateMultimodalityCompletionResponse"]


class InferenceGenerateMultimodalityCompletionResponse(BaseModel):
    """Response model for inference with text-to-speech and multimodal memory"""

    text_response: str
    """Generated text response from LLM"""

    audio_base64: Optional[str] = None
    """Base64 encoded audio of the response (if output_type='audio')"""

    audio_format: Optional[str] = None
    """Format of the audio (e.g., mp3)"""

    entity_images: Optional[Dict[str, str]] = None
    """
    Reference images for matched entities used in generation (entity_name -> base64
    image)
    """

    image_base64: Optional[str] = None
    """Base64 encoded AI-generated image (if output_type='image')"""

    memory_context: Optional[str] = None
    """Formatted memory context used for generating the response"""

    raw_results: Optional[Dict[str, object]] = None
    """Raw results from memory retrieval"""

    success: Optional[bool] = None
    """Whether the request was successful"""

    voice_used: Optional[str] = None
    """Voice used for TTS"""
