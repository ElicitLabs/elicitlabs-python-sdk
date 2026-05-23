# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Required, TypedDict

__all__ = ["DataIngestParams"]


class DataIngestParams(TypedDict, total=False):
    payload: Required[Union[str, Dict[str, object], Iterable[object]]]
    """Raw content as string, object, list (for messages), or base64 encoded data"""

    user_id: Required[str]
    """User ID (always required)"""

    callback_url: Optional[str]
    """
    Optional URL the server will POST to when the job reaches a terminal state
    (done, error, cancelled). The payload will match the /v1/data/job/status
    response shape.
    """

    content_description: Optional[str]
    """
    Optional description of the content being ingested (e.g., 'Logo design
    concepts', 'Meeting notes')
    """

    content_type: Optional[str]
    """Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.

    If omitted, the category is auto-detected from the uploaded file bytes.
    """

    crawl_options: Optional[Dict[str, object]]
    """Only used when content_type='website'.

    Optional knobs for the discovery + LLM filter step: max_sub_pages (default 50),
    include_subdomains, search, include_paths, exclude_paths, map_limit.
    """

    enable_planner: bool
    """
    Opt-in: when true, the ingester pauses after content prep and asks the user
    clarifying questions about ambiguous intent (e.g. 'is this a successful ad?',
    'should we retain product references?'). The job transitions to
    status='awaiting_planner_input' with planner_questions in the status response;
    the user submits answers via POST /v1/data/ingest/{job_id}/answer-planner. The
    planner can self-skip when the content is unambiguous.
    """

    filename: Optional[str]
    """Filename of the uploaded file"""

    notification_email: Optional[str]
    """Optional email address to notify when the job reaches a terminal state."""

    persona_id: Optional[str]
    """Optional persona ID.

    If provided, data is ingested to this persona instead of the user
    """

    project_id: Optional[str]
    """Optional project ID.

    If provided, data is ingested to this project (inherits from user)
    """

    session_id: Optional[str]
    """
    Session ID for grouping related ingested content and enabling session-based
    retrieval
    """

    target_ad_id: Optional[str]
    """
    When set, the ingest is interpreted as a free-form correction targeting an
    existing analyzed ad's LayoutAnalysis. `payload` must be a string (markdown /
    JSON / HTML / prose — any format). Claude reconciles the corrections against the
    ad's current four artifact JSONs (typography, sections, claude_labels,
    layout_metrics) with the user taking priority on every field they mention.
    Per-ad scope only — no fan-out to other ads in the project.
    """

    timestamp: Optional[str]
    """ISO-8601 timestamp to preserve original data moment"""
