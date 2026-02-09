# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import modal_learn_params, modal_query_params
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.modal_learn_response import ModalLearnResponse
from ..types.modal_query_response import ModalQueryResponse

__all__ = ["ModalResource", "AsyncModalResource"]


class ModalResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ModalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return ModalResourceWithStreamingResponse(self)

    def learn(
        self,
        *,
        messages: Iterable[modal_learn_params.Message],
        user_id: str,
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
    ) -> ModalLearnResponse:
        """
        Ingests a list of messages (conversation history) into long-term memory.

            The system automatically handles different modalities embedded in the messages:
            - **Text** is embedded directly
            - **Images/Video** are captioned/described by vision models, then embedded
            - **Audio** is transcribed, then embedded

            **Universal Base Params:**
            - user_id (str, required): The user these memories belong to
            - project_id (str, optional): The project bucket (optional)
            - persona_id (str, optional): Link these memories to a specific persona

            **Input (Multimodal):**
            - messages (array, required): A standard chat history list. Can contain Text, Image, Video, and Audio.
            - session_id (str, optional): Optional session identifier for conversation context

            **Example:**
            ```json
            {
                "user_id": "user_123",
                "project_id": "proj_ABC",
                "session_id": "session_123",
                "messages": [
                    {"role": "user", "type": "image", "content": "<base64 encoded image data>"},
                    {"role": "assistant","type": "text", "content": "The animation is too slow"},
                    {"role": "user", "content": "Good catch. Let's speed it up to 200ms."}
                    ],
                    "timestamp": "2026-02-07T12:00:00Z"
                }
                ```

        Args:
          messages: A standard chat history list. Can contain Text, Image, Video, and Audio.

          user_id: The user these memories belong to (required)

          persona_id: Optional persona ID. Link these memories to a specific persona.

          project_id: The project bucket (optional)

          session_id: Optional session identifier for conversation context

          timestamp: ISO format datetime string for the message timestamp

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/learn",
            body=maybe_transform(
                {
                    "messages": messages,
                    "user_id": user_id,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                modal_learn_params.ModalLearnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalLearnResponse,
        )

    def query(
        self,
        *,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        include_modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        text_input: Optional[str] | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModalQueryResponse:
        """
        Retrieves relevant memories based on text conversation context and/or multimodal
        inputs.

            You can provide **text messages**, **images**, **video**, **audio**, or any combination.
            The system finds memories semantically relevant to the provided inputs.

            **Universal Base Params:**
            - user_id (str, required): Restrict search to this user
            - project_id (str, required): Restrict search to this project
            - persona_id (str, optional): Use persona's context if provided

            **Input — at least one required:**
            - messages (array, optional): Text conversation context
            - video_base64 (str, optional): Base64 encoded video
            - image_base64 (str, optional): Base64 encoded image
            - audio_base64 (str, optional): Base64 encoded audio

            **Search Config:**
            - include_modalities (array, optional): Filter results by type: ["text", "image", "video"]

            **Response:**
            - new_prompt (str): Enhanced prompt with retrieved memory context
            - raw_results (dict): Structured memory data from retrieval
            - entity_images (dict, optional): Reference images for matched entities
            - success (bool): True if query succeeded

            Returns 200 OK with memory data. Requires authentication.

        Args:
          user_id: Restrict search to this user (required)

          audio_base64: Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)

          image_base64: Base64 encoded image content

          include_modalities: Filter results by type: ['text', 'image', 'video']

          persona_id: Optional persona ID. If provided, query uses persona's context

          project_id: Restrict search to this project (required)

          session_id: Optional session identifier for conversation context

          text_input: Text input to search against. The system finds memories _relevant_ to this text.

          video_base64: Base64 encoded video content

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/query",
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "audio_base64": audio_base64,
                    "image_base64": image_base64,
                    "include_modalities": include_modalities,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "text_input": text_input,
                    "video_base64": video_base64,
                },
                modal_query_params.ModalQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalQueryResponse,
        )


class AsyncModalResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncModalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncModalResourceWithStreamingResponse(self)

    async def learn(
        self,
        *,
        messages: Iterable[modal_learn_params.Message],
        user_id: str,
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
    ) -> ModalLearnResponse:
        """
        Ingests a list of messages (conversation history) into long-term memory.

            The system automatically handles different modalities embedded in the messages:
            - **Text** is embedded directly
            - **Images/Video** are captioned/described by vision models, then embedded
            - **Audio** is transcribed, then embedded

            **Universal Base Params:**
            - user_id (str, required): The user these memories belong to
            - project_id (str, optional): The project bucket (optional)
            - persona_id (str, optional): Link these memories to a specific persona

            **Input (Multimodal):**
            - messages (array, required): A standard chat history list. Can contain Text, Image, Video, and Audio.
            - session_id (str, optional): Optional session identifier for conversation context

            **Example:**
            ```json
            {
                "user_id": "user_123",
                "project_id": "proj_ABC",
                "session_id": "session_123",
                "messages": [
                    {"role": "user", "type": "image", "content": "<base64 encoded image data>"},
                    {"role": "assistant","type": "text", "content": "The animation is too slow"},
                    {"role": "user", "content": "Good catch. Let's speed it up to 200ms."}
                    ],
                    "timestamp": "2026-02-07T12:00:00Z"
                }
                ```

        Args:
          messages: A standard chat history list. Can contain Text, Image, Video, and Audio.

          user_id: The user these memories belong to (required)

          persona_id: Optional persona ID. Link these memories to a specific persona.

          project_id: The project bucket (optional)

          session_id: Optional session identifier for conversation context

          timestamp: ISO format datetime string for the message timestamp

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/learn",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "user_id": user_id,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "timestamp": timestamp,
                },
                modal_learn_params.ModalLearnParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalLearnResponse,
        )

    async def query(
        self,
        *,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        include_modalities: Optional[SequenceNotStr[str]] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        text_input: Optional[str] | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ModalQueryResponse:
        """
        Retrieves relevant memories based on text conversation context and/or multimodal
        inputs.

            You can provide **text messages**, **images**, **video**, **audio**, or any combination.
            The system finds memories semantically relevant to the provided inputs.

            **Universal Base Params:**
            - user_id (str, required): Restrict search to this user
            - project_id (str, required): Restrict search to this project
            - persona_id (str, optional): Use persona's context if provided

            **Input — at least one required:**
            - messages (array, optional): Text conversation context
            - video_base64 (str, optional): Base64 encoded video
            - image_base64 (str, optional): Base64 encoded image
            - audio_base64 (str, optional): Base64 encoded audio

            **Search Config:**
            - include_modalities (array, optional): Filter results by type: ["text", "image", "video"]

            **Response:**
            - new_prompt (str): Enhanced prompt with retrieved memory context
            - raw_results (dict): Structured memory data from retrieval
            - entity_images (dict, optional): Reference images for matched entities
            - success (bool): True if query succeeded

            Returns 200 OK with memory data. Requires authentication.

        Args:
          user_id: Restrict search to this user (required)

          audio_base64: Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)

          image_base64: Base64 encoded image content

          include_modalities: Filter results by type: ['text', 'image', 'video']

          persona_id: Optional persona ID. If provided, query uses persona's context

          project_id: Restrict search to this project (required)

          session_id: Optional session identifier for conversation context

          text_input: Text input to search against. The system finds memories _relevant_ to this text.

          video_base64: Base64 encoded video content

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/query",
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "audio_base64": audio_base64,
                    "image_base64": image_base64,
                    "include_modalities": include_modalities,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "text_input": text_input,
                    "video_base64": video_base64,
                },
                modal_query_params.ModalQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalQueryResponse,
        )


class ModalResourceWithRawResponse:
    def __init__(self, modal: ModalResource) -> None:
        self._modal = modal

        self.learn = to_raw_response_wrapper(
            modal.learn,
        )
        self.query = to_raw_response_wrapper(
            modal.query,
        )


class AsyncModalResourceWithRawResponse:
    def __init__(self, modal: AsyncModalResource) -> None:
        self._modal = modal

        self.learn = async_to_raw_response_wrapper(
            modal.learn,
        )
        self.query = async_to_raw_response_wrapper(
            modal.query,
        )


class ModalResourceWithStreamingResponse:
    def __init__(self, modal: ModalResource) -> None:
        self._modal = modal

        self.learn = to_streamed_response_wrapper(
            modal.learn,
        )
        self.query = to_streamed_response_wrapper(
            modal.query,
        )


class AsyncModalResourceWithStreamingResponse:
    def __init__(self, modal: AsyncModalResource) -> None:
        self._modal = modal

        self.learn = async_to_streamed_response_wrapper(
            modal.learn,
        )
        self.query = async_to_streamed_response_wrapper(
            modal.query,
        )
