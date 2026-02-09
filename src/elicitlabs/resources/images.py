# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from ..types import image_generate_params
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
from ..types.image_generate_response import ImageGenerateResponse

__all__ = ["ImagesResource", "AsyncImagesResource"]


class ImagesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ImagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ImagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ImagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return ImagesResourceWithStreamingResponse(self)

    def generate(
        self,
        *,
        text_input: str,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: str | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        size: Optional[str] | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ImageGenerateResponse:
        """
        Dedicated image generation endpoint using the Universal Schema with flat
        parameters.

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, required): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory
            - use_reasoning (bool, optional): Enable reasoning loop for constraint-satisfying generation

            **Input:**
            - text_input (str, optional): The prompt/description for image generation
            - session_id (str, optional): Session ID for conversation context

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Image Params (Flat):**
            - model (str, required): Model ID (e.g., flux-pro, dall-e-3)
            - size (str, optional): Image dimensions
            - seed (int, optional): Random seed for reproducibility

            **Authentication**: Requires valid API key or JWT token

        Args:
          text_input: The prompt/description for image generation

          user_id: The end-user ID

          audio_base64: Base64 encoded reference audio for context

          disabled_learning: If true, this request is ignored by long-term memory

          image_base64: Base64 encoded reference image for context

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: Image generation model ID

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          seed: Random seed for reproducibility

          session_id: Session ID for conversation context

          size: Image dimensions (e.g., 1024x1024)

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before generation

          video_base64: Base64 encoded reference video for context

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/images/generations",
            body=maybe_transform(
                {
                    "text_input": text_input,
                    "user_id": user_id,
                    "audio_base64": audio_base64,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "seed": seed,
                    "session_id": session_id,
                    "size": size,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                },
                image_generate_params.ImageGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImageGenerateResponse,
        )


class AsyncImagesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncImagesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncImagesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncImagesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncImagesResourceWithStreamingResponse(self)

    async def generate(
        self,
        *,
        text_input: str,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: str | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        size: Optional[str] | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ImageGenerateResponse:
        """
        Dedicated image generation endpoint using the Universal Schema with flat
        parameters.

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, required): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory
            - use_reasoning (bool, optional): Enable reasoning loop for constraint-satisfying generation

            **Input:**
            - text_input (str, optional): The prompt/description for image generation
            - session_id (str, optional): Session ID for conversation context

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Image Params (Flat):**
            - model (str, required): Model ID (e.g., flux-pro, dall-e-3)
            - size (str, optional): Image dimensions
            - seed (int, optional): Random seed for reproducibility

            **Authentication**: Requires valid API key or JWT token

        Args:
          text_input: The prompt/description for image generation

          user_id: The end-user ID

          audio_base64: Base64 encoded reference audio for context

          disabled_learning: If true, this request is ignored by long-term memory

          image_base64: Base64 encoded reference image for context

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: Image generation model ID

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          seed: Random seed for reproducibility

          session_id: Session ID for conversation context

          size: Image dimensions (e.g., 1024x1024)

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before generation

          video_base64: Base64 encoded reference video for context

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/images/generations",
            body=await async_maybe_transform(
                {
                    "text_input": text_input,
                    "user_id": user_id,
                    "audio_base64": audio_base64,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "seed": seed,
                    "session_id": session_id,
                    "size": size,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                },
                image_generate_params.ImageGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ImageGenerateResponse,
        )


class ImagesResourceWithRawResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.generate = to_raw_response_wrapper(
            images.generate,
        )


class AsyncImagesResourceWithRawResponse:
    def __init__(self, images: AsyncImagesResource) -> None:
        self._images = images

        self.generate = async_to_raw_response_wrapper(
            images.generate,
        )


class ImagesResourceWithStreamingResponse:
    def __init__(self, images: ImagesResource) -> None:
        self._images = images

        self.generate = to_streamed_response_wrapper(
            images.generate,
        )


class AsyncImagesResourceWithStreamingResponse:
    def __init__(self, images: AsyncImagesResource) -> None:
        self._images = images

        self.generate = async_to_streamed_response_wrapper(
            images.generate,
        )
