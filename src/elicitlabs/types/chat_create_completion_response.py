# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional

from .._models import BaseModel

__all__ = ["ChatCreateCompletionResponse", "Message", "MessageContentUnionMember1"]


class MessageContentUnionMember1(BaseModel):
    """A single content part within a multimodal message"""

    type: str
    """Content type: 'text', 'image', 'video', 'audio', or 'image_url'"""

    audio_url: Optional[Dict[str, str]] = None
    """Audio URL object with 'url' key"""

    content: Optional[str] = None
    """Base64 encoded content (for image/video/audio)"""

    image_url: Optional[Dict[str, str]] = None
    """Image URL object with 'url' key (can be data:image/... base64)"""

    text: Optional[str] = None
    """Text content (when type='text')"""

    video_url: Optional[Dict[str, str]] = None
    """Video URL object with 'url' key"""


class Message(BaseModel):
    """A single message in the conversation"""

    content: Union[str, List[MessageContentUnionMember1], List[Dict[str, object]]]
    """
    Message content - can be: - A simple text string - An array of content parts for
    multimodal input: [ {"type": "text", "text": "What's in this image?"}, {"type":
    "image", "content": "base64_encoded_image..."}, {"type": "image_url",
    "image_url": {"url": "data:image/jpeg;base64,..."}}, {"type": "video",
    "content": "base64_encoded_video..."}, {"type": "audio", "content":
    "base64_encoded_audio..."} ]
    """

    role: str
    """Message role: 'system', 'user', or 'assistant'"""


class ChatCreateCompletionResponse(BaseModel):
    """
    Response model for chat completions - returns the full conversation including the assistant's reply
    """

    messages: List[Message]
    """
    Full conversation: the original user messages plus the assistant's response
    appended
    """

    session_id: str
    """Session ID for conversation context"""
