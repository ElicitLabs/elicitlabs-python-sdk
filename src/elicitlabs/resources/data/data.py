# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional

import httpx

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
        payload: Union[str, Dict[str, object], Iterable[object]],
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
        Ingest data for asynchronous processing

            Accepts various content types (text, messages, files) and processes them to extract information
            and integrate it into the user's memory system. Returns a job_id for tracking status.

            **Entity Resolution:**
            - user_id (str, required): Always required - the main user identifier
            - persona_id (str, optional): If provided, data is ingested to this persona instead of user
            - project_id (str, optional): If provided, data is ingested to this project (inherits from user)

            Priority: persona_id > project_id > user_id

            **Request Parameters:**
            - content_type (str, required): One of: "text", "messages", "pdf", "word", "image", "video", "audio", "file"
            - payload (str|dict|list, required): Content data (text string, message list, or base64 for files)
            - content_description (str, optional): Description of the content being ingested (e.g., 'Logo design concepts', 'Meeting notes')
            - session_id (str, optional): Groups related content for session-based retrieval
            - timestamp (str, optional): ISO-8601 timestamp for historical data
            - filename (str, optional): Original filename for file uploads

            **Response:**
            - job_id (str): Unique identifier for tracking the processing job
            - user_id (str): Confirmed entity ID (user, persona, or project)
            - content_type (str): Confirmed content type
            - status (str): Job status ('queued', 'accepted')
            - message (str): Status message
            - created_at (str): ISO-8601 timestamp
            - success (bool): True if accepted

            **Example:**
            ```json
            {
                "user_id": "user-123",
                "persona_id": null,
                "project_id": "project-456",
                "content_type": "text",
                "payload": "Meeting notes from today's discussion",
                "content_description": "Meeting notes from today's discussion"
            }
            ```

            Returns 202 Accepted with job_id. Use /job/status to check processing status.
            Max payload: 5MB (JSON), 20MB (multipart). Requires JWT authentication.

        Args:
          payload: Raw content as string, object, list (for messages), or base64 encoded data

          user_id: User ID (always required)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state
              (done, error, cancelled). The payload will match the /v1/data/job/status
              response shape.

          content_description: Optional description of the content being ingested (e.g., 'Logo design
              concepts', 'Meeting notes')

          content_type: Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.
              If omitted, the category is auto-detected from the uploaded file bytes.

          filename: Filename of the uploaded file

          notification_email: Optional email address to notify when the job reaches a terminal state.

          persona_id: Optional persona ID. If provided, data is ingested to this persona instead of
              the user

          project_id: Optional project ID. If provided, data is ingested to this project (inherits
              from user)

          session_id: Session ID for grouping related ingested content and enabling session-based
              retrieval

          timestamp: ISO-8601 timestamp to preserve original data moment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/data/ingest",
            body=maybe_transform(
                {
                    "payload": payload,
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
                data_ingest_params.DataIngestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataIngestResponse,
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
        payload: Union[str, Dict[str, object], Iterable[object]],
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
        Ingest data for asynchronous processing

            Accepts various content types (text, messages, files) and processes them to extract information
            and integrate it into the user's memory system. Returns a job_id for tracking status.

            **Entity Resolution:**
            - user_id (str, required): Always required - the main user identifier
            - persona_id (str, optional): If provided, data is ingested to this persona instead of user
            - project_id (str, optional): If provided, data is ingested to this project (inherits from user)

            Priority: persona_id > project_id > user_id

            **Request Parameters:**
            - content_type (str, required): One of: "text", "messages", "pdf", "word", "image", "video", "audio", "file"
            - payload (str|dict|list, required): Content data (text string, message list, or base64 for files)
            - content_description (str, optional): Description of the content being ingested (e.g., 'Logo design concepts', 'Meeting notes')
            - session_id (str, optional): Groups related content for session-based retrieval
            - timestamp (str, optional): ISO-8601 timestamp for historical data
            - filename (str, optional): Original filename for file uploads

            **Response:**
            - job_id (str): Unique identifier for tracking the processing job
            - user_id (str): Confirmed entity ID (user, persona, or project)
            - content_type (str): Confirmed content type
            - status (str): Job status ('queued', 'accepted')
            - message (str): Status message
            - created_at (str): ISO-8601 timestamp
            - success (bool): True if accepted

            **Example:**
            ```json
            {
                "user_id": "user-123",
                "persona_id": null,
                "project_id": "project-456",
                "content_type": "text",
                "payload": "Meeting notes from today's discussion",
                "content_description": "Meeting notes from today's discussion"
            }
            ```

            Returns 202 Accepted with job_id. Use /job/status to check processing status.
            Max payload: 5MB (JSON), 20MB (multipart). Requires JWT authentication.

        Args:
          payload: Raw content as string, object, list (for messages), or base64 encoded data

          user_id: User ID (always required)

          callback_url: Optional URL the server will POST to when the job reaches a terminal state
              (done, error, cancelled). The payload will match the /v1/data/job/status
              response shape.

          content_description: Optional description of the content being ingested (e.g., 'Logo design
              concepts', 'Meeting notes')

          content_type: Content category: 'text', 'image', 'video', 'pdf', 'audio', 'messages', 'file'.
              If omitted, the category is auto-detected from the uploaded file bytes.

          filename: Filename of the uploaded file

          notification_email: Optional email address to notify when the job reaches a terminal state.

          persona_id: Optional persona ID. If provided, data is ingested to this persona instead of
              the user

          project_id: Optional project ID. If provided, data is ingested to this project (inherits
              from user)

          session_id: Session ID for grouping related ingested content and enabling session-based
              retrieval

          timestamp: ISO-8601 timestamp to preserve original data moment

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/data/ingest",
            body=await async_maybe_transform(
                {
                    "payload": payload,
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
                data_ingest_params.DataIngestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DataIngestResponse,
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
