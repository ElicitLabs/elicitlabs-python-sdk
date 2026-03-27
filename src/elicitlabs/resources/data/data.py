# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import copy
import os
import base64
import hashlib
import logging
import mimetypes
from typing import Dict, Union, Iterable, Optional
from pathlib import Path
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

from .job import (
    JobResource,
    AsyncJobResource,
    JobResourceWithRawResponse,
    AsyncJobResourceWithRawResponse,
    JobResourceWithStreamingResponse,
    AsyncJobResourceWithStreamingResponse,
)
from ...types import data_ingest_params, data_confirm_upload_params, data_get_upload_url_params
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.data_ingest_response import DataIngestResponse
from ...types.data_confirm_upload_response import DataConfirmUploadResponse
from ...types.data_get_upload_url_response import DataGetUploadURLResponse

__all__ = ["DataResource", "AsyncDataResource"]

_UPLOAD_THRESHOLD = 20 * 1024 * 1024  # 20 MB
_FILE_TRANSFER_TIMEOUT = httpx.Timeout(connect=10.0, read=300.0, write=300.0, pool=10.0)
_MAX_UPLOAD_RETRIES = 3
_MEDIA_PART_TYPES = frozenset({"image", "audio", "video"})


def _is_already_gcs_key(value: str) -> bool:
    """GCS object keys have no scheme, no ``data:`` prefix, and at least
    three path segments (e.g. ``prod/user-uuid/ingest/2026/file.png``).

    Absolute (``/``), home-relative (``~``), and dot-relative (``.``) paths
    are excluded — GCS keys always start with an alphanumeric segment.
    """
    return (
        "://" not in value
        and not value.startswith(("data:", "/", ".", "~"))
        and value.count("/") >= 3
    )


def _resolve_media_bytes(value: str) -> tuple[bytes, str] | None:
    """Attempt to decode *value* as a ``data:`` URI or raw base64 string.

    Returns ``(file_bytes, extension)`` on success, ``None`` when *value*
    does not look like inline data.
    """
    if value.startswith("data:"):
        try:
            header, b64_data = value.split(",", 1)
        except ValueError:
            return None
        mime = header.split(";")[0].replace("data:", "")
        ext = mime.split("/")[-1] if "/" in mime else "bin"
        return base64.b64decode(b64_data), ext

    # Last resort: try raw base64 — if it fails, the value is something else
    # (plain text, already a GCS key, etc.) and we leave it alone.
    try:
        decoded = base64.b64decode(value, validate=True)
        if len(decoded) > 0:
            return decoded, "bin"
    except Exception:
        pass

    return None


def _is_url(value: object) -> bool:
    return isinstance(value, str) and value.startswith(("http://", "https://"))


def _looks_like_path(value: str) -> bool:
    """Conservatively check if a string looks like a file path rather than
    base64-encoded data or plain text.  Requires at least one path separator
    (``/`` or ``\\``) or a leading ``.`` / ``~``."""
    return ("/" in value or "\\" in value or value.startswith((".", "~")))


def _is_file_path(value: object) -> bool:
    if isinstance(value, Path):
        return value.is_file()
    if isinstance(value, str) and not _is_url(value) and _looks_like_path(value):
        try:
            return Path(value).is_file()
        except (OSError, ValueError):
            return False
    return False


def _download_from_url(url: str) -> tuple[bytes, str]:
    """Download content from a URL with verification.

    Returns (file_bytes, resolved_filename).
    Raises on inaccessible URLs, non-success responses, and truncated downloads.
    """
    try:
        download_resp = httpx.get(url, follow_redirects=True, timeout=_FILE_TRANSFER_TIMEOUT)
    except httpx.ConnectError as exc:
        raise ConnectionError(f"Could not connect to URL: {url}") from exc
    except httpx.TimeoutException as exc:
        raise TimeoutError(f"Timed out downloading from URL: {url}") from exc
    except httpx.RequestError as exc:
        raise ConnectionError(f"Failed to download from URL: {url} — {exc}") from exc

    if download_resp.status_code != 200:
        raise ValueError(
            f"URL returned HTTP {download_resp.status_code}: {url}"
        )

    file_bytes = download_resp.content

    # Verify download was not truncated
    expected_length = download_resp.headers.get("content-length")
    if expected_length is not None:
        expected_length = int(expected_length)
        if len(file_bytes) != expected_length:
            raise ValueError(
                f"Download truncated: expected {expected_length} bytes but received {len(file_bytes)} from {url}"
            )

    if len(file_bytes) == 0:
        raise ValueError(f"Downloaded 0 bytes from URL (empty response): {url}")

    # Verify content looks like the expected type, not an error page
    resp_content_type = download_resp.headers.get("content-type", "")
    if "text/html" in resp_content_type and not url.endswith((".html", ".htm")):
        logger.warning(
            "URL returned Content-Type 'text/html' which may indicate an error page "
            "rather than the expected file: %s",
            url,
        )

    # Resolve filename — prefer Content-Disposition, fall back to URL path
    resolved_filename = None
    content_disposition = download_resp.headers.get("content-disposition", "")
    if "filename=" in content_disposition:
        # Extract filename from Content-Disposition header
        for part in content_disposition.split(";"):
            part = part.strip()
            if part.startswith("filename="):
                resolved_filename = part.split("=", 1)[1].strip().strip('"\'')
                break

    if not resolved_filename:
        resolved_filename = os.path.basename(urlparse(url).path) or "downloaded_file"

    # If filename still lacks an extension, try to infer from Content-Type
    if "." not in resolved_filename and resp_content_type:
        mime_base = resp_content_type.split(";")[0].strip()
        ext = mimetypes.guess_extension(mime_base)
        if ext:
            resolved_filename += ext

    return file_bytes, resolved_filename


async def _async_download_from_url(url: str) -> tuple[bytes, str]:
    """Async version of _download_from_url."""
    try:
        async with httpx.AsyncClient(timeout=_FILE_TRANSFER_TIMEOUT) as http:
            download_resp = await http.get(url, follow_redirects=True)
    except httpx.ConnectError as exc:
        raise ConnectionError(f"Could not connect to URL: {url}") from exc
    except httpx.TimeoutException as exc:
        raise TimeoutError(f"Timed out downloading from URL: {url}") from exc
    except httpx.RequestError as exc:
        raise ConnectionError(f"Failed to download from URL: {url} — {exc}") from exc

    if download_resp.status_code != 200:
        raise ValueError(
            f"URL returned HTTP {download_resp.status_code}: {url}"
        )

    file_bytes = download_resp.content

    expected_length = download_resp.headers.get("content-length")
    if expected_length is not None:
        expected_length = int(expected_length)
        if len(file_bytes) != expected_length:
            raise ValueError(
                f"Download truncated: expected {expected_length} bytes but received {len(file_bytes)} from {url}"
            )

    if len(file_bytes) == 0:
        raise ValueError(f"Downloaded 0 bytes from URL (empty response): {url}")

    resp_content_type = download_resp.headers.get("content-type", "")
    if "text/html" in resp_content_type and not url.endswith((".html", ".htm")):
        logger.warning(
            "URL returned Content-Type 'text/html' which may indicate an error page "
            "rather than the expected file: %s",
            url,
        )

    resolved_filename = None
    content_disposition = download_resp.headers.get("content-disposition", "")
    if "filename=" in content_disposition:
        for part in content_disposition.split(";"):
            part = part.strip()
            if part.startswith("filename="):
                resolved_filename = part.split("=", 1)[1].strip().strip('"\'')
                break

    if not resolved_filename:
        resolved_filename = os.path.basename(urlparse(url).path) or "downloaded_file"

    if "." not in resolved_filename and resp_content_type:
        mime_base = resp_content_type.split(";")[0].strip()
        ext = mimetypes.guess_extension(mime_base)
        if ext:
            resolved_filename += ext

    return file_bytes, resolved_filename


def _verify_gcs_upload(put_resp: httpx.Response, file_bytes: bytes) -> None:
    """Verify the GCS upload integrity by comparing the ETag MD5 hash."""
    etag = put_resp.headers.get("etag", "").strip('"')
    if not etag or "-" in etag:
        # Multipart uploads have ETags with a dash — skip verification
        return

    local_md5 = hashlib.md5(file_bytes).hexdigest()
    if etag.lower() != local_md5.lower():
        raise ValueError(
            f"Upload integrity check failed: local MD5 {local_md5} != GCS ETag {etag}. "
            f"The file may have been corrupted during upload."
        )


def _mime_to_content_category(mime: str) -> str:
    """Map a MIME type (e.g. 'video/mp4') to the API content_type category
    (e.g. 'video').  Returns ``None`` for unrecognised types so the caller
    can omit the field and let the server auto-detect."""
    if mime.startswith("image/"):
        return "image"
    if mime.startswith("video/"):
        return "video"
    if mime.startswith("audio/"):
        return "audio"
    if mime == "application/pdf":
        return "pdf"
    if mime in (
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ):
        return "word"
    if mime.startswith("text/"):
        return "text"
    return "file"


class DataResource(SyncAPIResource):
    @cached_property
    def job(self) -> JobResource:
        return JobResource(self._client)

    @cached_property
    def with_raw_response(self) -> DataResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DataResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return DataResourceWithStreamingResponse(self)

    def confirm_upload(
        self,
        *,
        job_id: str,
        object_key: str,
        user_id: str,
        callback_url: Optional[str] | Omit = omit,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        timestamp: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DataConfirmUploadResponse:
        """
        **Step 2 of 2** — After uploading the file to the signed URL obtained from
        `/ingest/upload-url`, call this endpoint to trigger the ingest pipeline.

            The server verifies the file exists in GCS, auto-detects the content type
            if it was not provided, and queues the processing job.

            Returns the same `IngestResponse` as the regular `/ingest` endpoint.

        Args:
          job_id: Job ID returned by /ingest/upload-url

          object_key: GCS object key returned by /ingest/upload-url

          user_id: User ID (must match the upload-url request)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state.

          content_type: Content category (auto-detected from file bytes if omitted)

          notification_email: Optional email address to notify when the job reaches a terminal state.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/data/ingest/confirm-upload",
            body=maybe_transform(
                {
                    "job_id": job_id,
                    "object_key": object_key,
                    "user_id": user_id,
                    "callback_url": callback_url,
                    "content_description": content_description,
                    "content_type": content_type,
                    "filename": filename,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_confirm_upload_params.DataConfirmUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataConfirmUploadResponse,
        )

    def get_upload_url(
        self,
        *,
        user_id: str,
        callback_url: Optional[str] | Omit = omit,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        timestamp: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DataGetUploadURLResponse:
        """
        **Step 1 of 2** — Obtain a time-limited signed URL for uploading a file directly
        to cloud storage (GCS).

            Use this instead of `/ingest` when the payload is large (e.g. > 32 MB)
            to avoid sending the entire file through the API server.

            **Flow:**
            1. Call this endpoint → receive `upload_url`, `job_id`, `object_key`
            2. HTTP **PUT** the raw file bytes to `upload_url`
            3. Call `/ingest/confirm-upload` with the `job_id` and `object_key`
               to kick off the processing pipeline

            The signed URL expires after the time indicated by `expires_in` (default 1 hour).

        Args:
          user_id: User ID (always required)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state.

          content_description: Optional description of the content being ingested

          content_type: Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.
              If omitted, the category is auto-detected after the file is uploaded.

          filename: Filename of the file to upload

          notification_email: Optional email address to notify when the job reaches a terminal state.

          persona_id: Optional persona ID. If provided, data is ingested to this persona

          project_id: Optional project ID. If provided, data is ingested to this project

          session_id: Session ID for grouping related ingested content

          timestamp: ISO-8601 timestamp to preserve original data moment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/data/ingest/upload-url",
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "callback_url": callback_url,
                    "content_description": content_description,
                    "content_type": content_type,
                    "filename": filename,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_get_upload_url_params.DataGetUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataGetUploadURLResponse,
        )

    def ingest(
        self,
        *,
        payload: Union[str, Path, Dict[str, object], Iterable[object]],
        user_id: str,
        callback_url: Optional[str] | Omit = omit,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        timestamp: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DataIngestResponse:
        """
        Ingest data for asynchronous processing.

        Accepts various content types (text, messages, files) and processes them
        to extract information and integrate it into the user's memory system.

        **Smart payload handling:** The ``payload`` parameter accepts:

        - **Plain text or structured data** — passed directly to the API.
        - **A local file path** (``str`` or ``pathlib.Path``) — the SDK reads the
          file, base64-encodes it for small files (< 20 MB), or uses a signed-URL
          upload for larger files.
        - **A URL** (``http://`` / ``https://``) — the SDK downloads the content
          and uploads it the same way.

        Args:
          payload: Text string, message list, base64 data, a local file path, or a URL.
              File paths and URLs are resolved automatically.

          user_id: User ID (always required)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state
              (done, error, cancelled). The payload will match the /v1/data/job/status
              response shape.

          content_description: Optional description of the content being ingested (e.g., 'Logo design
              concepts', 'Meeting notes')

          content_type: Content type (e.g., 'text', 'image', 'video', 'pdf', 'word', 'audio',
              'messages', 'file')

          filename: Filename for file uploads (auto-detected from path/URL when omitted)

          notification_email: Optional email address to notify when the job reaches a terminal state.

          persona_id: Optional persona ID. If provided, data is ingested to this persona

          project_id: Optional project ID. If provided, data is ingested to this project

          session_id: Session ID for grouping related ingested content

          timestamp: ISO-8601 timestamp to preserve original data moment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        file_bytes: bytes | None = None
        resolved_filename: str | None = None

        if isinstance(payload, Path):
            if not payload.is_file():
                raise FileNotFoundError(f"File not found: {payload}")
            file_bytes = payload.read_bytes()
            resolved_filename = payload.name
        elif isinstance(payload, str):
            if _is_url(payload):
                file_bytes, resolved_filename = _download_from_url(payload)
            elif _is_file_path(payload):
                path = Path(payload)
                file_bytes = path.read_bytes()
                resolved_filename = path.name

        if file_bytes is not None:
            actual_filename = (
                filename if (filename is not omit and filename is not None) else resolved_filename
            )

            return self._ingest_via_signed_url(
                file_bytes=file_bytes,
                filename=actual_filename or "uploaded_file",
                user_id=user_id,
                persona_id=persona_id if isinstance(persona_id, str) else None,
                project_id=project_id if isinstance(project_id, str) else None,
                content_description=content_description if isinstance(content_description, str) else None,
                session_id=session_id if isinstance(session_id, str) else None,
                timestamp=timestamp if isinstance(timestamp, str) else None,
            )

        if isinstance(payload, list):
            payload = self._resolve_message_files(
                payload=payload,
                user_id=user_id,
                project_id=project_id if isinstance(project_id, str) else None,
                persona_id=persona_id if isinstance(persona_id, str) else None,
            )

        return self._post(
            "/v1/data/ingest",
            body=maybe_transform(
                {
                    "content_type": content_type,
                    "payload": payload,
                    "user_id": user_id,
                    "callback_url": callback_url,
                    "content_description": content_description,
                    "filename": filename,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_ingest_params.DataIngestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataIngestResponse,
        )

    # ── Private helpers for the signed-URL upload flow ───────────────────

    def _get_upload_url(
        self,
        *,
        user_id: str,
        filename: str,
        content_type: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
    ) -> DataGetUploadURLResponse:
        return self._post(
            "/v1/data/ingest/upload-url",
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "filename": filename,
                    "content_type": content_type,
                    "project_id": project_id,
                    "persona_id": persona_id,
                },
                data_get_upload_url_params.DataGetUploadURLParams,
            ),
            options=make_request_options(),
            cast_to=DataGetUploadURLResponse,
        )

    def _confirm_upload(
        self,
        *,
        job_id: str,
        object_key: str,
        user_id: str,
        content_type: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        filename: Optional[str] = None,
        content_description: Optional[str] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DataConfirmUploadResponse:
        return self._post(
            "/v1/data/ingest/confirm-upload",
            body=maybe_transform(
                {
                    "job_id": job_id,
                    "object_key": object_key,
                    "user_id": user_id,
                    "content_type": content_type,
                    "project_id": project_id,
                    "persona_id": persona_id,
                    "filename": filename,
                    "content_description": content_description,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_confirm_upload_params.DataConfirmUploadParams,
            ),
            options=make_request_options(),
            cast_to=DataConfirmUploadResponse,
        )

    def _ingest_via_signed_url(
        self,
        *,
        file_bytes: bytes,
        filename: str,
        user_id: str,
        persona_id: Optional[str] = None,
        project_id: Optional[str] = None,
        content_description: Optional[str] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DataIngestResponse:
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content_category = _mime_to_content_category(mime_type)
        expected_size = len(file_bytes)

        last_error: Exception | None = None
        for attempt in range(1, _MAX_UPLOAD_RETRIES + 1):
            upload_info = self._get_upload_url(
                user_id=user_id,
                filename=filename,
                content_type=content_category,
                project_id=project_id if project_id else omit,
                persona_id=persona_id if persona_id else omit,
            )

            try:
                put_resp = httpx.put(
                    upload_info.upload_url,
                    content=file_bytes,
                    headers={
                        "Content-Type": mime_type,
                        "Content-Length": str(expected_size),
                    },
                    timeout=_FILE_TRANSFER_TIMEOUT,
                )
                put_resp.raise_for_status()
                _verify_gcs_upload(put_resp, file_bytes)
            except (httpx.RequestError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Signed URL upload attempt %d/%d failed: %s",
                    attempt, _MAX_UPLOAD_RETRIES, exc,
                )
                if attempt < _MAX_UPLOAD_RETRIES:
                    continue
                raise ValueError(
                    f"File upload failed after {_MAX_UPLOAD_RETRIES} attempts. Last error: {last_error}"
                ) from last_error

            # Upload succeeded and integrity verified
            break

        confirm = self._confirm_upload(
            job_id=upload_info.job_id,
            object_key=upload_info.object_key,
            user_id=user_id,
            content_type=content_category,
            project_id=project_id if project_id else omit,
            persona_id=persona_id if persona_id else omit,
            filename=filename,
            content_description=content_description,
            session_id=session_id,
            timestamp=timestamp,
        )

        return DataIngestResponse(
            job_id=confirm.job_id,
            status=confirm.status,
            message=confirm.message,
            success=True,
        )


    def _upload_to_gcs(
        self,
        *,
        file_bytes: bytes,
        filename: str,
        user_id: str,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
    ) -> str:
        """Upload file bytes to GCS via signed URL and return the object key.

        Unlike ``_ingest_via_signed_url`` this does **not** call
        ``confirm_upload`` — it is meant for attaching files to a messages
        payload where the top-level ``/ingest`` call handles processing.
        """
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content_category = _mime_to_content_category(mime_type)

        last_error: Exception | None = None
        upload_info: DataGetUploadURLResponse | None = None
        for attempt in range(1, _MAX_UPLOAD_RETRIES + 1):
            upload_info = self._get_upload_url(
                user_id=user_id,
                filename=filename,
                content_type=content_category,
                project_id=project_id if project_id else omit,
                persona_id=persona_id if persona_id else omit,
            )

            try:
                put_resp = httpx.put(
                    upload_info.upload_url,
                    content=file_bytes,
                    headers={
                        "Content-Type": mime_type,
                        "Content-Length": str(len(file_bytes)),
                    },
                    timeout=_FILE_TRANSFER_TIMEOUT,
                )
                put_resp.raise_for_status()
                _verify_gcs_upload(put_resp, file_bytes)
            except (httpx.RequestError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Signed URL upload attempt %d/%d failed: %s",
                    attempt, _MAX_UPLOAD_RETRIES, exc,
                )
                if attempt < _MAX_UPLOAD_RETRIES:
                    continue
                raise ValueError(
                    f"File upload failed after {_MAX_UPLOAD_RETRIES} attempts. "
                    f"Last error: {last_error}"
                ) from last_error

            break

        assert upload_info is not None
        return upload_info.object_key

    def _resolve_message_files(
        self,
        *,
        payload: list[object],
        user_id: str,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
    ) -> list[object]:
        """Walk a messages payload, upload inline media to GCS, and return a
        copy with references replaced by GCS object keys.

        Handles ``{"type": "image"|"audio"|"video", "content": ...}`` parts
        and ``{"type": "image_url", "image_url": {"url": ...}}`` parts.

        *content* / *url* values that are already GCS keys are left untouched.
        Local file paths, HTTP(S) URLs, ``data:`` URIs, and raw base64 strings
        are resolved, uploaded, and replaced.
        """
        resolved = copy.deepcopy(payload)

        for message in resolved:
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue

                part_type = part.get("type", "")

                if part_type in _MEDIA_PART_TYPES:
                    value = part.get("content")
                    gcs_key = self._resolve_value_to_gcs_key(
                        value, part_type, user_id, project_id, persona_id,
                    )
                    if gcs_key is not None:
                        part["content"] = gcs_key

                elif part_type == "image_url":
                    url_obj = part.get("image_url")
                    if not isinstance(url_obj, dict):
                        continue
                    value = url_obj.get("url")
                    gcs_key = self._resolve_value_to_gcs_key(
                        value, "image", user_id, project_id, persona_id,
                    )
                    if gcs_key is not None:
                        part["image_url"] = {"url": gcs_key}

        return resolved

    def _resolve_value_to_gcs_key(
        self,
        value: object,
        media_type: str,
        user_id: str,
        project_id: Optional[str],
        persona_id: Optional[str],
    ) -> str | None:
        """Resolve a single content value to a GCS object key.

        Returns the key if the value was uploaded, or ``None`` if it should be
        left as-is (empty, already a GCS key, or unrecognised).
        """
        if not value:
            return None

        file_bytes: bytes | None = None
        resolved_filename: str | None = None

        if isinstance(value, Path):
            if not value.is_file():
                raise FileNotFoundError(f"File not found: {value}")
            file_bytes = value.read_bytes()
            resolved_filename = value.name
        elif isinstance(value, str):
            if _is_already_gcs_key(value):
                return None
            if _is_url(value):
                file_bytes, resolved_filename = _download_from_url(value)
            elif _is_file_path(value):
                p = Path(value)
                file_bytes = p.read_bytes()
                resolved_filename = p.name
            else:
                result = _resolve_media_bytes(value)
                if result is not None:
                    file_bytes, ext = result
                    resolved_filename = f"inline_media.{ext}"
        else:
            return None

        if file_bytes is None:
            return None

        return self._upload_to_gcs(
            file_bytes=file_bytes,
            filename=resolved_filename or f"inline_media.{media_type}",
            user_id=user_id,
            project_id=project_id,
            persona_id=persona_id,
        )


class AsyncDataResource(AsyncAPIResource):
    @cached_property
    def job(self) -> AsyncJobResource:
        return AsyncJobResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDataResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDataResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncDataResourceWithStreamingResponse(self)

    async def confirm_upload(
        self,
        *,
        job_id: str,
        object_key: str,
        user_id: str,
        callback_url: Optional[str] | Omit = omit,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        timestamp: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DataConfirmUploadResponse:
        """
        **Step 2 of 2** — After uploading the file to the signed URL obtained from
        `/ingest/upload-url`, call this endpoint to trigger the ingest pipeline.

            The server verifies the file exists in GCS, auto-detects the content type
            if it was not provided, and queues the processing job.

            Returns the same `IngestResponse` as the regular `/ingest` endpoint.

        Args:
          job_id: Job ID returned by /ingest/upload-url

          object_key: GCS object key returned by /ingest/upload-url

          user_id: User ID (must match the upload-url request)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state.

          content_type: Content category (auto-detected from file bytes if omitted)

          notification_email: Optional email address to notify when the job reaches a terminal state.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/data/ingest/confirm-upload",
            body=await async_maybe_transform(
                {
                    "job_id": job_id,
                    "object_key": object_key,
                    "user_id": user_id,
                    "callback_url": callback_url,
                    "content_description": content_description,
                    "content_type": content_type,
                    "filename": filename,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_confirm_upload_params.DataConfirmUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataConfirmUploadResponse,
        )

    async def get_upload_url(
        self,
        *,
        user_id: str,
        callback_url: Optional[str] | Omit = omit,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        timestamp: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DataGetUploadURLResponse:
        """
        **Step 1 of 2** — Obtain a time-limited signed URL for uploading a file directly
        to cloud storage (GCS).

            Use this instead of `/ingest` when the payload is large (e.g. > 32 MB)
            to avoid sending the entire file through the API server.

            **Flow:**
            1. Call this endpoint → receive `upload_url`, `job_id`, `object_key`
            2. HTTP **PUT** the raw file bytes to `upload_url`
            3. Call `/ingest/confirm-upload` with the `job_id` and `object_key`
               to kick off the processing pipeline

            The signed URL expires after the time indicated by `expires_in` (default 1 hour).

        Args:
          user_id: User ID (always required)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state.

          content_description: Optional description of the content being ingested

          content_type: Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.
              If omitted, the category is auto-detected after the file is uploaded.

          filename: Filename of the file to upload

          notification_email: Optional email address to notify when the job reaches a terminal state.

          persona_id: Optional persona ID. If provided, data is ingested to this persona

          project_id: Optional project ID. If provided, data is ingested to this project

          session_id: Session ID for grouping related ingested content

          timestamp: ISO-8601 timestamp to preserve original data moment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/data/ingest/upload-url",
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "callback_url": callback_url,
                    "content_description": content_description,
                    "content_type": content_type,
                    "filename": filename,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_get_upload_url_params.DataGetUploadURLParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataGetUploadURLResponse,
        )

    async def ingest(
        self,
        *,
        payload: Union[str, Path, Dict[str, object], Iterable[object]],
        user_id: str,
        callback_url: Optional[str] | Omit = omit,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        timestamp: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DataIngestResponse:
        """
        Ingest data for asynchronous processing.

        Accepts various content types (text, messages, files) and processes them
        to extract information and integrate it into the user's memory system.

        **Smart payload handling:** The ``payload`` parameter accepts:

        - **Plain text or structured data** — passed directly to the API.
        - **A local file path** (``str`` or ``pathlib.Path``) — the SDK reads the
          file, base64-encodes it for small files (< 20 MB), or uses a signed-URL
          upload for larger files.
        - **A URL** (``http://`` / ``https://``) — the SDK downloads the content
          and uploads it the same way.

        Args:
          payload: Text string, message list, base64 data, a local file path, or a URL.
              File paths and URLs are resolved automatically.

          user_id: User ID (always required)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state
              (done, error, cancelled). The payload will match the /v1/data/job/status
              response shape.

          content_description: Optional description of the content being ingested (e.g., 'Logo design
              concepts', 'Meeting notes')

          content_type: Content type (e.g., 'text', 'image', 'video', 'pdf', 'word', 'audio',
              'messages', 'file')

          filename: Filename for file uploads (auto-detected from path/URL when omitted)

          notification_email: Optional email address to notify when the job reaches a terminal state.

          persona_id: Optional persona ID. If provided, data is ingested to this persona

          project_id: Optional project ID. If provided, data is ingested to this project

          session_id: Session ID for grouping related ingested content

          timestamp: ISO-8601 timestamp to preserve original data moment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        file_bytes: bytes | None = None
        resolved_filename: str | None = None

        if isinstance(payload, Path):
            if not payload.is_file():
                raise FileNotFoundError(f"File not found: {payload}")
            file_bytes = payload.read_bytes()
            resolved_filename = payload.name
        elif isinstance(payload, str):
            if _is_url(payload):
                file_bytes, resolved_filename = await _async_download_from_url(payload)
            elif _is_file_path(payload):
                path = Path(payload)
                file_bytes = path.read_bytes()
                resolved_filename = path.name

        if file_bytes is not None:
            actual_filename = (
                filename if (filename is not omit and filename is not None) else resolved_filename
            )

            return await self._ingest_via_signed_url(
                file_bytes=file_bytes,
                filename=actual_filename or "uploaded_file",
                user_id=user_id,
                persona_id=persona_id if isinstance(persona_id, str) else None,
                project_id=project_id if isinstance(project_id, str) else None,
                content_description=content_description if isinstance(content_description, str) else None,
                session_id=session_id if isinstance(session_id, str) else None,
                timestamp=timestamp if isinstance(timestamp, str) else None,
            )

        if isinstance(payload, list):
            payload = await self._resolve_message_files(
                payload=payload,
                user_id=user_id,
                project_id=project_id if isinstance(project_id, str) else None,
                persona_id=persona_id if isinstance(persona_id, str) else None,
            )

        return await self._post(
            "/v1/data/ingest",
            body=await async_maybe_transform(
                {
                    "content_type": content_type,
                    "payload": payload,
                    "user_id": user_id,
                    "callback_url": callback_url,
                    "content_description": content_description,
                    "filename": filename,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_ingest_params.DataIngestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataIngestResponse,
        )

    # ── Private helpers for the signed-URL upload flow ───────────────────

    async def _get_upload_url(
        self,
        *,
        user_id: str,
        filename: str,
        content_type: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
    ) -> DataGetUploadURLResponse:
        return await self._post(
            "/v1/data/ingest/upload-url",
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "filename": filename,
                    "content_type": content_type,
                    "project_id": project_id,
                    "persona_id": persona_id,
                },
                data_get_upload_url_params.DataGetUploadURLParams,
            ),
            options=make_request_options(),
            cast_to=DataGetUploadURLResponse,
        )

    async def _confirm_upload(
        self,
        *,
        job_id: str,
        object_key: str,
        user_id: str,
        content_type: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        filename: Optional[str] = None,
        content_description: Optional[str] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DataConfirmUploadResponse:
        return await self._post(
            "/v1/data/ingest/confirm-upload",
            body=await async_maybe_transform(
                {
                    "job_id": job_id,
                    "object_key": object_key,
                    "user_id": user_id,
                    "content_type": content_type,
                    "project_id": project_id,
                    "persona_id": persona_id,
                    "filename": filename,
                    "content_description": content_description,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                data_confirm_upload_params.DataConfirmUploadParams,
            ),
            options=make_request_options(),
            cast_to=DataConfirmUploadResponse,
        )

    async def _ingest_via_signed_url(
        self,
        *,
        file_bytes: bytes,
        filename: str,
        user_id: str,
        persona_id: Optional[str] = None,
        project_id: Optional[str] = None,
        content_description: Optional[str] = None,
        session_id: Optional[str] = None,
        timestamp: Optional[str] = None,
    ) -> DataIngestResponse:
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content_category = _mime_to_content_category(mime_type)
        expected_size = len(file_bytes)

        last_error: Exception | None = None
        for attempt in range(1, _MAX_UPLOAD_RETRIES + 1):
            upload_info = await self._get_upload_url(
                user_id=user_id,
                filename=filename,
                content_type=content_category,
                project_id=project_id if project_id else omit,
                persona_id=persona_id if persona_id else omit,
            )

            try:
                async with httpx.AsyncClient(timeout=_FILE_TRANSFER_TIMEOUT) as http:
                    put_resp = await http.put(
                        upload_info.upload_url,
                        content=file_bytes,
                        headers={
                            "Content-Type": mime_type,
                            "Content-Length": str(expected_size),
                        },
                    )
                    put_resp.raise_for_status()
                _verify_gcs_upload(put_resp, file_bytes)
            except (httpx.RequestError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Signed URL upload attempt %d/%d failed: %s",
                    attempt, _MAX_UPLOAD_RETRIES, exc,
                )
                if attempt < _MAX_UPLOAD_RETRIES:
                    continue
                raise ValueError(
                    f"File upload failed after {_MAX_UPLOAD_RETRIES} attempts. Last error: {last_error}"
                ) from last_error

            break

        confirm = await self._confirm_upload(
            job_id=upload_info.job_id,
            object_key=upload_info.object_key,
            user_id=user_id,
            content_type=content_category,
            project_id=project_id if project_id else omit,
            persona_id=persona_id if persona_id else omit,
            filename=filename,
            content_description=content_description,
            session_id=session_id,
            timestamp=timestamp,
        )

        return DataIngestResponse(
            job_id=confirm.job_id,
            status=confirm.status,
            message=confirm.message,
            success=True,
        )

    async def _upload_to_gcs(
        self,
        *,
        file_bytes: bytes,
        filename: str,
        user_id: str,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
    ) -> str:
        """Async version: upload file bytes to GCS and return the object key
        (no ``confirm_upload``)."""
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content_category = _mime_to_content_category(mime_type)

        last_error: Exception | None = None
        upload_info: DataGetUploadURLResponse | None = None
        for attempt in range(1, _MAX_UPLOAD_RETRIES + 1):
            upload_info = await self._get_upload_url(
                user_id=user_id,
                filename=filename,
                content_type=content_category,
                project_id=project_id if project_id else omit,
                persona_id=persona_id if persona_id else omit,
            )

            try:
                async with httpx.AsyncClient(timeout=_FILE_TRANSFER_TIMEOUT) as http:
                    put_resp = await http.put(
                        upload_info.upload_url,
                        content=file_bytes,
                        headers={
                            "Content-Type": mime_type,
                            "Content-Length": str(len(file_bytes)),
                        },
                    )
                    put_resp.raise_for_status()
                _verify_gcs_upload(put_resp, file_bytes)
            except (httpx.RequestError, ValueError) as exc:
                last_error = exc
                logger.warning(
                    "Signed URL upload attempt %d/%d failed: %s",
                    attempt, _MAX_UPLOAD_RETRIES, exc,
                )
                if attempt < _MAX_UPLOAD_RETRIES:
                    continue
                raise ValueError(
                    f"File upload failed after {_MAX_UPLOAD_RETRIES} attempts. "
                    f"Last error: {last_error}"
                ) from last_error

            break

        assert upload_info is not None
        return upload_info.object_key

    async def _resolve_message_files(
        self,
        *,
        payload: list[object],
        user_id: str,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
    ) -> list[object]:
        """Async version: walk messages, upload inline media to GCS, and
        return a copy with references replaced by GCS object keys.

        Handles ``{"type": "image"|"audio"|"video", "content": ...}`` parts
        and ``{"type": "image_url", "image_url": {"url": ...}}`` parts.
        """
        resolved = copy.deepcopy(payload)

        for message in resolved:
            if not isinstance(message, dict):
                continue
            content = message.get("content")
            if not isinstance(content, list):
                continue
            for part in content:
                if not isinstance(part, dict):
                    continue

                part_type = part.get("type", "")

                if part_type in _MEDIA_PART_TYPES:
                    value = part.get("content")
                    gcs_key = await self._resolve_value_to_gcs_key(
                        value, part_type, user_id, project_id, persona_id,
                    )
                    if gcs_key is not None:
                        part["content"] = gcs_key

                elif part_type == "image_url":
                    url_obj = part.get("image_url")
                    if not isinstance(url_obj, dict):
                        continue
                    value = url_obj.get("url")
                    gcs_key = await self._resolve_value_to_gcs_key(
                        value, "image", user_id, project_id, persona_id,
                    )
                    if gcs_key is not None:
                        part["image_url"] = {"url": gcs_key}

        return resolved

    async def _resolve_value_to_gcs_key(
        self,
        value: object,
        media_type: str,
        user_id: str,
        project_id: Optional[str],
        persona_id: Optional[str],
    ) -> str | None:
        """Async version: resolve a single content value to a GCS object key."""
        if not value:
            return None

        file_bytes: bytes | None = None
        resolved_filename: str | None = None

        if isinstance(value, Path):
            if not value.is_file():
                raise FileNotFoundError(f"File not found: {value}")
            file_bytes = value.read_bytes()
            resolved_filename = value.name
        elif isinstance(value, str):
            if _is_already_gcs_key(value):
                return None
            if _is_url(value):
                file_bytes, resolved_filename = await _async_download_from_url(value)
            elif _is_file_path(value):
                p = Path(value)
                file_bytes = p.read_bytes()
                resolved_filename = p.name
            else:
                result = _resolve_media_bytes(value)
                if result is not None:
                    file_bytes, ext = result
                    resolved_filename = f"inline_media.{ext}"
        else:
            return None

        if file_bytes is None:
            return None

        return await self._upload_to_gcs(
            file_bytes=file_bytes,
            filename=resolved_filename or f"inline_media.{media_type}",
            user_id=user_id,
            project_id=project_id,
            persona_id=persona_id,
        )


class DataResourceWithRawResponse:
    def __init__(self, data: DataResource) -> None:
        self._data = data

        self.confirm_upload = to_raw_response_wrapper(
            data.confirm_upload,
        )
        self.get_upload_url = to_raw_response_wrapper(
            data.get_upload_url,
        )
        self.ingest = to_raw_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> JobResourceWithRawResponse:
        return JobResourceWithRawResponse(self._data.job)


class AsyncDataResourceWithRawResponse:
    def __init__(self, data: AsyncDataResource) -> None:
        self._data = data

        self.confirm_upload = async_to_raw_response_wrapper(
            data.confirm_upload,
        )
        self.get_upload_url = async_to_raw_response_wrapper(
            data.get_upload_url,
        )
        self.ingest = async_to_raw_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> AsyncJobResourceWithRawResponse:
        return AsyncJobResourceWithRawResponse(self._data.job)


class DataResourceWithStreamingResponse:
    def __init__(self, data: DataResource) -> None:
        self._data = data

        self.confirm_upload = to_streamed_response_wrapper(
            data.confirm_upload,
        )
        self.get_upload_url = to_streamed_response_wrapper(
            data.get_upload_url,
        )
        self.ingest = to_streamed_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> JobResourceWithStreamingResponse:
        return JobResourceWithStreamingResponse(self._data.job)


class AsyncDataResourceWithStreamingResponse:
    def __init__(self, data: AsyncDataResource) -> None:
        self._data = data

        self.confirm_upload = async_to_streamed_response_wrapper(
            data.confirm_upload,
        )
        self.get_upload_url = async_to_streamed_response_wrapper(
            data.get_upload_url,
        )
        self.ingest = async_to_streamed_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> AsyncJobResourceWithStreamingResponse:
        return AsyncJobResourceWithStreamingResponse(self._data.job)
