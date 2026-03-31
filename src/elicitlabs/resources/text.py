# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional, Union

import httpx

from ..types import text_generate_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
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
from ..types.async_generation_response import AsyncGenerationResponse
from ..types.text_generate_response import TextGenerateResponse

__all__ = ["TextResource", "AsyncTextResource"]


class TextResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return TextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return TextResourceWithStreamingResponse(self)

    def generate(
        self,
        *,
        user_id: str,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        callback_url: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: str | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        output_schema: Optional[Dict[str, object]] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        text_input: Optional[str] | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Union[TextGenerateResponse, AsyncGenerationResponse]:
        """
        Dedicated text generation endpoint using the Universal Schema with flat
        parameters.

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, required): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory
            - use_reasoning (bool, optional): Enable reasoning loop for generation

            **Input:**
            - text_input (str, optional): The prompt/description for text generation
            - session_id (str, optional): Session ID for conversation context

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Text Params (Flat):**
            - model (str, optional): LLM model to use (default: gpt-4.1-mini)

            **Authentication**: Requires valid API key or JWT token

        Args:
          user_id: The end-user ID

          audio_base64: Base64 encoded reference audio for context

          disabled_learning: If true, this request is ignored by long-term memory

          image_base64: Base64 encoded reference image for context

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: LLM model to use for generation

          output_schema: Optional JSON Schema describing the desired output structure. When provided, the
              LLM is forced to return a JSON object matching this schema instead of free-form
              text. The result is returned in the 'structured_output' field of the response.

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          session_id: Session ID for conversation context

          text_input: The prompt/description for text generation

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before generation

          video_base64: Base64 encoded reference video for context

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/text/generations",
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "callback_url": callback_url,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "notification_email": notification_email,
                    "output_schema": output_schema,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "text_input": text_input,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                },
                text_generate_params.TextGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TextGenerateResponse,
        )


class AsyncTextResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTextResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncTextResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTextResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncTextResourceWithStreamingResponse(self)

    async def generate(
        self,
        *,
        user_id: str,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        callback_url: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: str | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        output_schema: Optional[Dict[str, object]] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        text_input: Optional[str] | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Union[TextGenerateResponse, AsyncGenerationResponse]:
        """
        Dedicated text generation endpoint using the Universal Schema with flat
        parameters.

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, required): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory
            - use_reasoning (bool, optional): Enable reasoning loop for generation

            **Input:**
            - text_input (str, optional): The prompt/description for text generation
            - session_id (str, optional): Session ID for conversation context

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Text Params (Flat):**
            - model (str, optional): LLM model to use (default: gpt-4.1-mini)

            **Authentication**: Requires valid API key or JWT token

        Args:
          user_id: The end-user ID

          audio_base64: Base64 encoded reference audio for context

          disabled_learning: If true, this request is ignored by long-term memory

          image_base64: Base64 encoded reference image for context

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: LLM model to use for generation

          output_schema: Optional JSON Schema describing the desired output structure. When provided, the
              LLM is forced to return a JSON object matching this schema instead of free-form
              text. The result is returned in the 'structured_output' field of the response.

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          session_id: Session ID for conversation context

          text_input: The prompt/description for text generation

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before generation

          video_base64: Base64 encoded reference video for context

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/text/generations",
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "callback_url": callback_url,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "notification_email": notification_email,
                    "output_schema": output_schema,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                    "text_input": text_input,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                },
                text_generate_params.TextGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TextGenerateResponse,
        )


class TextResourceWithRawResponse:
    def __init__(self, text: TextResource) -> None:
        self._text = text

        self.generate = to_raw_response_wrapper(
            text.generate,
        )


class AsyncTextResourceWithRawResponse:
    def __init__(self, text: AsyncTextResource) -> None:
        self._text = text

        self.generate = async_to_raw_response_wrapper(
            text.generate,
        )


class TextResourceWithStreamingResponse:
    def __init__(self, text: TextResource) -> None:
        self._text = text

        self.generate = to_streamed_response_wrapper(
            text.generate,
        )


class AsyncTextResourceWithStreamingResponse:
    def __init__(self, text: AsyncTextResource) -> None:
        self._text = text

        self.generate = async_to_streamed_response_wrapper(
            text.generate,
        )
