# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["InferenceGenerateCompletionParams"]


class InferenceGenerateCompletionParams(TypedDict, total=False):
    content: Required[Union[str, Iterable[Dict[str, str]]]]
    """Content to process"""

    user_id: Required[str]
    """User ID (always required)"""

    disabled_learning: bool
    """Whether to disable learning"""

    model: str
    """LLM model to use for generation"""

    persona_id: Optional[str]
    """Optional persona ID.

    If provided, inference uses this persona's context instead of the user
    """

    project_id: Optional[str]
    """Optional project ID.

    If provided, inference uses project context (inherits from user)
    """

    session_id: Optional[str]
    """Session ID"""
