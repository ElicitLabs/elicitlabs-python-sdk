# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

import httpx

from ..types import chat_create_completion_params
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
from ..types.chat_create_completion_response import ChatCreateCompletionResponse

__all__ = ["ChatResource", "AsyncChatResource"]


class ChatResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return ChatResourceWithStreamingResponse(self)

    def create_completion(
        self,
        *,
        messages: Iterable[chat_create_completion_params.Message],
        user_id: str,
        audio_config: Optional[chat_create_completion_params.AudioConfig] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_config: Optional[chat_create_completion_params.ImageConfig] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        modalities: SequenceNotStr[str] | Omit = omit,
        model: str | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        stream: bool | Omit = omit,
        use_reasoning: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCreateCompletionResponse:
        """
        Unified generation endpoint that accepts the Universal Schema plus configuration
        objects for any outputs (Text, Image, Audio, or all at once).

            This is the "Omni" endpoint for the Elicit Labs Modal System.
            It acts as a thin orchestrator:

            **Flow:**
            1. Extracts text + multimodal content from the messages array
            2. Classifies the desired output modality via LLM (text / image / audio)
            3. Delegates to the appropriate generation endpoint handler:
               - text  → POST /v1/text/generations
               - image → POST /v1/images/generations
               - audio → POST /v1/audio/generations
            4. Returns unified response with text + optional image/audio

            All validation, memory retrieval, and generation logic lives in the
            dedicated routers. This endpoint just classifies and dispatches.

            **Authentication**: Requires valid API key or JWT token

        Args:
          messages: List of messages (system, user, assistant) with text, images, video, or audio

          user_id: The end-user ID

          audio_config: Configuration overrides for audio generation

          disabled_learning: If true, this request is ignored by long-term memory

          image_config: Configuration overrides for image generation

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          modalities: List of desired outputs: 'text', 'image', 'audio'

          model: LLM model to use for generation

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          session_id: Session ID for conversation context

          stream: Enable streaming response (SSE)

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before answering

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/chat/completions",
            body=maybe_transform(
                {
                    "messages": messages,
                    "user_id": user_id,
                    "audio_config": audio_config,
                    "disabled_learning": disabled_learning,
                    "image_config": image_config,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "modalities": modalities,
                    "model": model,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "stream": stream,
                    "use_reasoning": use_reasoning,
                },
                chat_create_completion_params.ChatCreateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCreateCompletionResponse,
        )


class AsyncChatResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncChatResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncChatResourceWithStreamingResponse(self)

    async def create_completion(
        self,
        *,
        messages: Iterable[chat_create_completion_params.Message],
        user_id: str,
        audio_config: Optional[chat_create_completion_params.AudioConfig] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_config: Optional[chat_create_completion_params.ImageConfig] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        modalities: SequenceNotStr[str] | Omit = omit,
        model: str | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        stream: bool | Omit = omit,
        use_reasoning: bool | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ChatCreateCompletionResponse:
        """
        Unified generation endpoint that accepts the Universal Schema plus configuration
        objects for any outputs (Text, Image, Audio, or all at once).

            This is the "Omni" endpoint for the Elicit Labs Modal System.
            It acts as a thin orchestrator:

            **Flow:**
            1. Extracts text + multimodal content from the messages array
            2. Classifies the desired output modality via LLM (text / image / audio)
            3. Delegates to the appropriate generation endpoint handler:
               - text  → POST /v1/text/generations
               - image → POST /v1/images/generations
               - audio → POST /v1/audio/generations
            4. Returns unified response with text + optional image/audio

            All validation, memory retrieval, and generation logic lives in the
            dedicated routers. This endpoint just classifies and dispatches.

            **Authentication**: Requires valid API key or JWT token

        Args:
          messages: List of messages (system, user, assistant) with text, images, video, or audio

          user_id: The end-user ID

          audio_config: Configuration overrides for audio generation

          disabled_learning: If true, this request is ignored by long-term memory

          image_config: Configuration overrides for image generation

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          modalities: List of desired outputs: 'text', 'image', 'audio'

          model: LLM model to use for generation

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          session_id: Session ID for conversation context

          stream: Enable streaming response (SSE)

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before answering

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/chat/completions",
            body=await async_maybe_transform(
                {
                    "messages": messages,
                    "user_id": user_id,
                    "audio_config": audio_config,
                    "disabled_learning": disabled_learning,
                    "image_config": image_config,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "modalities": modalities,
                    "model": model,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "stream": stream,
                    "use_reasoning": use_reasoning,
                },
                chat_create_completion_params.ChatCreateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatCreateCompletionResponse,
        )


class ChatResourceWithRawResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create_completion = to_raw_response_wrapper(
            chat.create_completion,
        )


class AsyncChatResourceWithRawResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create_completion = async_to_raw_response_wrapper(
            chat.create_completion,
        )


class ChatResourceWithStreamingResponse:
    def __init__(self, chat: ChatResource) -> None:
        self._chat = chat

        self.create_completion = to_streamed_response_wrapper(
            chat.create_completion,
        )


class AsyncChatResourceWithStreamingResponse:
    def __init__(self, chat: AsyncChatResource) -> None:
        self._chat = chat

        self.create_completion = async_to_streamed_response_wrapper(
            chat.create_completion,
        )
