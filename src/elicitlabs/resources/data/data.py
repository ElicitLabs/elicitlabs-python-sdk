# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
import base64
import mimetypes
from typing import Dict, Union, Iterable, Optional
from pathlib import Path
from urllib.parse import urlparse

import httpx

from .job import (
    JobResource,
    AsyncJobResource,
    JobResourceWithRawResponse,
    AsyncJobResourceWithRawResponse,
    JobResourceWithStreamingResponse,
    AsyncJobResourceWithStreamingResponse,
)
from ...types import data_ingest_params, data_upload_url_params, data_confirm_upload_params
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
from ...types.data_upload_url_response import DataUploadUrlResponse
from ...types.data_confirm_upload_response import DataConfirmUploadResponse

__all__ = ["DataResource", "AsyncDataResource"]

_UPLOAD_THRESHOLD = 20 * 1024 * 1024  # 20 MB
_FILE_TRANSFER_TIMEOUT = httpx.Timeout(connect=10.0, read=300.0, write=300.0, pool=10.0)


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

    def ingest(
        self,
        *,
        payload: Union[str, Path, Dict[str, object], Iterable[object]],
        user_id: str,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
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

          content_description: Optional description of the content being ingested

          content_type: Content type (e.g., 'text', 'image', 'video', 'pdf', 'word', 'audio',
              'messages', 'file')

          filename: Filename for file uploads (auto-detected from path/URL when omitted)

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
                download_resp = httpx.get(payload, follow_redirects=True, timeout=_FILE_TRANSFER_TIMEOUT)
                download_resp.raise_for_status()
                file_bytes = download_resp.content
                resolved_filename = os.path.basename(urlparse(payload).path) or "downloaded_file"
            elif _is_file_path(payload):
                path = Path(payload)
                file_bytes = path.read_bytes()
                resolved_filename = path.name

        if file_bytes is not None:
            actual_filename = (
                filename if (filename is not omit and filename is not None) else resolved_filename
            )

            if len(file_bytes) >= _UPLOAD_THRESHOLD:
                return self._ingest_via_signed_url(
                    file_bytes=file_bytes,
                    filename=actual_filename or "uploaded_file",
                    user_id=user_id,
                    persona_id=persona_id if isinstance(persona_id, str) else None,
                    project_id=project_id if isinstance(project_id, str) else None,
                )

            payload = base64.b64encode(file_bytes).decode("utf-8")
            if actual_filename:
                filename = actual_filename

        return self._post(
            "/v1/data/ingest",
            body=maybe_transform(
                {
                    "content_type": content_type,
                    "payload": payload,
                    "user_id": user_id,
                    "content_description": content_description,
                    "filename": filename,
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
    ) -> DataUploadUrlResponse:
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
                data_upload_url_params.DataUploadUrlParams,
            ),
            options=make_request_options(),
            cast_to=DataUploadUrlResponse,
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
    ) -> DataIngestResponse:
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content_category = _mime_to_content_category(mime_type)

        upload_info = self._get_upload_url(
            user_id=user_id,
            filename=filename,
            content_type=content_category,
            project_id=project_id if project_id else omit,
            persona_id=persona_id if persona_id else omit,
        )

        put_resp = httpx.put(
            upload_info.upload_url,
            content=file_bytes,
            headers={"Content-Type": mime_type},
            timeout=_FILE_TRANSFER_TIMEOUT,
        )
        put_resp.raise_for_status()

        confirm = self._confirm_upload(
            job_id=upload_info.job_id,
            object_key=upload_info.object_key,
            user_id=user_id,
            content_type=content_category,
            project_id=project_id if project_id else omit,
            persona_id=persona_id if persona_id else omit,
        )

        return DataIngestResponse(
            job_id=confirm.job_id,
            status=confirm.status,
            message=confirm.message,
            success=True,
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

    async def ingest(
        self,
        *,
        payload: Union[str, Path, Dict[str, object], Iterable[object]],
        user_id: str,
        content_description: Optional[str] | Omit = omit,
        content_type: Optional[str] | Omit = omit,
        filename: Optional[str] | Omit = omit,
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

          content_description: Optional description of the content being ingested

          content_type: Content type (e.g., 'text', 'image', 'video', 'pdf', 'word', 'audio',
              'messages', 'file')

          filename: Filename for file uploads (auto-detected from path/URL when omitted)

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
                async with httpx.AsyncClient(timeout=_FILE_TRANSFER_TIMEOUT) as http:
                    download_resp = await http.get(payload, follow_redirects=True)
                    download_resp.raise_for_status()
                file_bytes = download_resp.content
                resolved_filename = os.path.basename(urlparse(payload).path) or "downloaded_file"
            elif _is_file_path(payload):
                path = Path(payload)
                file_bytes = path.read_bytes()
                resolved_filename = path.name

        if file_bytes is not None:
            actual_filename = (
                filename if (filename is not omit and filename is not None) else resolved_filename
            )

            if len(file_bytes) >= _UPLOAD_THRESHOLD:
                return await self._ingest_via_signed_url(
                    file_bytes=file_bytes,
                    filename=actual_filename or "uploaded_file",
                    user_id=user_id,
                    persona_id=persona_id if isinstance(persona_id, str) else None,
                    project_id=project_id if isinstance(project_id, str) else None,
                )

            payload = base64.b64encode(file_bytes).decode("utf-8")
            if actual_filename:
                filename = actual_filename

        return await self._post(
            "/v1/data/ingest",
            body=await async_maybe_transform(
                {
                    "content_type": content_type,
                    "payload": payload,
                    "user_id": user_id,
                    "content_description": content_description,
                    "filename": filename,
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
    ) -> DataUploadUrlResponse:
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
                data_upload_url_params.DataUploadUrlParams,
            ),
            options=make_request_options(),
            cast_to=DataUploadUrlResponse,
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
    ) -> DataIngestResponse:
        mime_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        content_category = _mime_to_content_category(mime_type)

        upload_info = await self._get_upload_url(
            user_id=user_id,
            filename=filename,
            content_type=content_category,
            project_id=project_id if project_id else omit,
            persona_id=persona_id if persona_id else omit,
        )

        async with httpx.AsyncClient(timeout=_FILE_TRANSFER_TIMEOUT) as http:
            put_resp = await http.put(
                upload_info.upload_url,
                content=file_bytes,
                headers={"Content-Type": mime_type},
            )
            put_resp.raise_for_status()

        confirm = await self._confirm_upload(
            job_id=upload_info.job_id,
            object_key=upload_info.object_key,
            user_id=user_id,
            content_type=content_category,
            project_id=project_id if project_id else omit,
            persona_id=persona_id if persona_id else omit,
        )

        return DataIngestResponse(
            job_id=confirm.job_id,
            status=confirm.status,
            message=confirm.message,
            success=True,
        )


class DataResourceWithRawResponse:
    def __init__(self, data: DataResource) -> None:
        self._data = data

        self.ingest = to_raw_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> JobResourceWithRawResponse:
        return JobResourceWithRawResponse(self._data.job)


class AsyncDataResourceWithRawResponse:
    def __init__(self, data: AsyncDataResource) -> None:
        self._data = data

        self.ingest = async_to_raw_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> AsyncJobResourceWithRawResponse:
        return AsyncJobResourceWithRawResponse(self._data.job)


class DataResourceWithStreamingResponse:
    def __init__(self, data: DataResource) -> None:
        self._data = data

        self.ingest = to_streamed_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> JobResourceWithStreamingResponse:
        return JobResourceWithStreamingResponse(self._data.job)


class AsyncDataResourceWithStreamingResponse:
    def __init__(self, data: AsyncDataResource) -> None:
        self._data = data

        self.ingest = async_to_streamed_response_wrapper(
            data.ingest,
        )

    @cached_property
    def job(self) -> AsyncJobResourceWithStreamingResponse:
        return AsyncJobResourceWithStreamingResponse(self._data.job)
