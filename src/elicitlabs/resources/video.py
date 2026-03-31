# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional, Union

import httpx

from ..types import video_generate_params
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
from ..types.video_generate_response import VideoGenerateResponse

__all__ = ["VideoResource", "AsyncVideoResource"]


class VideoResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VideoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return VideoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VideoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return VideoResourceWithStreamingResponse(self)

    def generate(
        self,
        *,
        text_input: str,
        user_id: str,
        advanced_creative: bool | Omit = omit,
        aspect_ratio: str | Omit = omit,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        callback_url: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        duration: Optional[float] | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: str | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Union[VideoGenerateResponse, AsyncGenerationResponse]:
        """
        Dedicated video generation endpoint using the Universal Schema with flat
        parameters.

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, optional): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory
            - use_reasoning (bool, optional): Enable reasoning loop for constraint-satisfying generation

            **Input:**
            - text_input (str, required): The prompt/description for video generation
            - session_id (str, optional): Session ID for conversation context

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Video Params (Flat):**
            - model (str, optional): Model ID (default: veo-3.0-generate-preview)
            - duration (float, optional): Target duration in seconds (4, 6, or 8)
            - aspect_ratio (str, optional): Aspect ratio: "16:9" or "9:16" (default: 16:9)
            - seed (int, optional): Random seed for reproducibility

            **Authentication**: Requires valid API key or JWT token

        Args:
          text_input: The prompt/description for video generation

          user_id: The end-user ID

          advanced_creative: Enable first+last frame workflow: generates a starting frame and an ending frame
              via the image pipeline, then uses Veo's first-and-last-frame feature to animate
              the transition between them.

          aspect_ratio: Aspect ratio for the generated video: '16:9' or '9:16'.

          audio_base64: Base64 encoded reference audio for context

          disabled_learning: If true, this request is ignored by long-term memory

          duration: Target duration in seconds

          image_base64: Base64 encoded reference image for context (e.g., start frame)

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: Video generation model ID

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          seed: Random seed for reproducibility

          session_id: Session ID for conversation context

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before generation

          video_base64: Base64 encoded reference video for context

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/video/generations",
            body=maybe_transform(
                {
                    "text_input": text_input,
                    "user_id": user_id,
                    "advanced_creative": advanced_creative,
                    "aspect_ratio": aspect_ratio,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "callback_url": callback_url,
                    "disabled_learning": disabled_learning,
                    "duration": duration,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "seed": seed,
                    "session_id": session_id,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                },
                video_generate_params.VideoGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VideoGenerateResponse,
        )


class AsyncVideoResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVideoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncVideoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVideoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncVideoResourceWithStreamingResponse(self)

    async def generate(
        self,
        *,
        text_input: str,
        user_id: str,
        advanced_creative: bool | Omit = omit,
        aspect_ratio: str | Omit = omit,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        callback_url: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        duration: Optional[float] | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: str | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> Union[VideoGenerateResponse, AsyncGenerationResponse]:
        """
        Dedicated video generation endpoint using the Universal Schema with flat
        parameters.

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, optional): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory
            - use_reasoning (bool, optional): Enable reasoning loop for constraint-satisfying generation

            **Input:**
            - text_input (str, required): The prompt/description for video generation
            - session_id (str, optional): Session ID for conversation context

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Video Params (Flat):**
            - model (str, optional): Model ID (default: veo-3.0-generate-preview)
            - duration (float, optional): Target duration in seconds (4, 6, or 8)
            - aspect_ratio (str, optional): Aspect ratio: "16:9" or "9:16" (default: 16:9)
            - seed (int, optional): Random seed for reproducibility

            **Authentication**: Requires valid API key or JWT token

        Args:
          text_input: The prompt/description for video generation

          user_id: The end-user ID

          advanced_creative: Enable first+last frame workflow: generates a starting frame and an ending frame
              via the image pipeline, then uses Veo's first-and-last-frame feature to animate
              the transition between them.

          aspect_ratio: Aspect ratio for the generated video: '16:9' or '9:16'.

          audio_base64: Base64 encoded reference audio for context

          disabled_learning: If true, this request is ignored by long-term memory

          duration: Target duration in seconds

          image_base64: Base64 encoded reference image for context (e.g., start frame)

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: Video generation model ID

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          seed: Random seed for reproducibility

          session_id: Session ID for conversation context

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before generation

          video_base64: Base64 encoded reference video for context

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/video/generations",
            body=await async_maybe_transform(
                {
                    "text_input": text_input,
                    "user_id": user_id,
                    "advanced_creative": advanced_creative,
                    "aspect_ratio": aspect_ratio,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "callback_url": callback_url,
                    "disabled_learning": disabled_learning,
                    "duration": duration,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "seed": seed,
                    "session_id": session_id,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                },
                video_generate_params.VideoGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VideoGenerateResponse,
        )


class VideoResourceWithRawResponse:
    def __init__(self, video: VideoResource) -> None:
        self._video = video

        self.generate = to_raw_response_wrapper(
            video.generate,
        )


class AsyncVideoResourceWithRawResponse:
    def __init__(self, video: AsyncVideoResource) -> None:
        self._video = video

        self.generate = async_to_raw_response_wrapper(
            video.generate,
        )


class VideoResourceWithStreamingResponse:
    def __init__(self, video: VideoResource) -> None:
        self._video = video

        self.generate = to_streamed_response_wrapper(
            video.generate,
        )


class AsyncVideoResourceWithStreamingResponse:
    def __init__(self, video: AsyncVideoResource) -> None:
        self._video = video

        self.generate = async_to_streamed_response_wrapper(
            video.generate,
        )
