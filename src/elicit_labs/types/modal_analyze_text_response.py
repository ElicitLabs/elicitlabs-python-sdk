# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = ["ModalAnalyzeTextResponse"]


class ModalAnalyzeTextResponse(BaseModel):
    apply_order: str
    """Order to apply edits (desc = descending)"""

    edits: List[Dict[str, object]]
    """List of edit operations"""

    final_text: str
    """Fully corrected text"""

    indexing: str
    """Indexing scheme used (utf16)"""

    issues_by_type: Dict[str, int]
    """Count of issues by type"""

    policy: Dict[str, object]
    """Policy settings"""

    processing_time_seconds: float
    """Time taken to analyze"""

    source_sha256: str
    """SHA256 checksum of original text"""

    version: str
    """Version identifier"""

    success: Optional[bool] = None
    """Whether the analysis was successful"""
