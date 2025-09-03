# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .._models import BaseModel
from .app_context import AppContext

__all__ = [
    "ModalInitializeResponse",
    "SessionContext",
    "SessionContextRetrievedContext",
    "SessionContextScreenshotAnalysis",
    "SessionContextScreenshotAnalysisExtractedFeatures",
]


class SessionContextRetrievedContext(BaseModel):
    retrieval_query: str
    """Query used for retrieval"""

    episodic_memories: Optional[List[Dict[str, object]]] = None
    """Retrieved episodic memories"""

    identity_attributes: Optional[List[Dict[str, object]]] = None
    """Retrieved identity attributes"""

    preferences: Optional[List[Dict[str, object]]] = None
    """Retrieved preferences"""

    retrieval_timestamp: Optional[datetime] = None
    """When the retrieval was performed"""

    total_retrieved: Optional[int] = None
    """Total number of items retrieved"""


class SessionContextScreenshotAnalysisExtractedFeatures(BaseModel):
    bcc: Optional[List[str]] = None
    """BCC recipients"""

    cc: Optional[List[str]] = None
    """CC recipients"""

    content: Optional[str] = None
    """Email body content"""

    date: Optional[str] = None
    """Email date/timestamp"""

    email_type: Optional[Literal["reply", "forward", "new"]] = None
    """Type of email action"""

    from_: Optional[str] = FieldInfo(alias="from", default=None)
    """Email sender"""

    retrieval_context: Optional[str] = None
    """
    Descriptive sentence summarizing who, what action, and what topic (e.g., 'John
    sent an email to Sarah about quarterly budget review')
    """

    subject: Optional[str] = None
    """Email subject line"""

    to: Optional[List[str]] = None
    """Email recipients"""


class SessionContextScreenshotAnalysis(BaseModel):
    extracted_features: SessionContextScreenshotAnalysisExtractedFeatures
    """Extracted email features"""

    analysis_notes: Optional[str] = None
    """Additional analysis notes"""

    raw_text: Optional[str] = None
    """Raw text extracted from screenshot"""


class SessionContext(BaseModel):
    app_context: AppContext
    """Application context"""

    retrieved_context: SessionContextRetrievedContext
    """Context from memory retrieval"""

    screenshot_analysis: SessionContextScreenshotAnalysis
    """Screenshot analysis results"""

    session_id: str
    """Unique session identifier"""

    user_id: str
    """User identifier"""

    created_at: Optional[datetime] = None
    """Session creation timestamp"""

    status: Optional[Literal["initialized", "processing", "completed", "failed"]] = None
    """Session status"""


class ModalInitializeResponse(BaseModel):
    processing_time_seconds: float
    """Time taken to process the request"""

    session_context: SessionContext
    """Complete session context"""

    success: bool
    """Whether initialization was successful"""

    error_message: Optional[str] = None
    """Error message if initialization failed"""
