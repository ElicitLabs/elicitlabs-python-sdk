# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import typing_extensions
from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal

import httpx

from ..types import inference_generate_completion_params, inference_generate_multimodality_completion_params
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
from ..types.inference_generate_completion_response import InferenceGenerateCompletionResponse
from ..types.inference_generate_multimodality_completion_response import (
    InferenceGenerateMultimodalityCompletionResponse,
)

__all__ = ["InferenceResource", "AsyncInferenceResource"]


class InferenceResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> InferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return InferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> InferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return InferenceResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    def generate_completion(
        self,
        *,
        content: Union[str, Iterable[Dict[str, str]]],
        user_id: str,
        disabled_learning: bool | Omit = omit,
        model: str | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGenerateCompletionResponse:
        """
        **⚠️ DEPRECATED** — Use `POST /v1/chat/completions` or
        `POST /v1/text/generations` instead.

            This endpoint is kept for backward compatibility and internally delegates to
            the new text generation handler.

        Args:
          content: Content to process

          user_id: User ID (always required)

          disabled_learning: Whether to disable learning

          model: LLM model to use for generation

          persona_id: Optional persona ID. If provided, inference uses this persona's context instead
              of the user

          project_id: Optional project ID. If provided, inference uses project context (inherits from
              user)

          session_id: Session ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/inference/completion",
            body=maybe_transform(
                {
                    "content": content,
                    "user_id": user_id,
                    "disabled_learning": disabled_learning,
                    "model": model,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                },
                inference_generate_completion_params.InferenceGenerateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGenerateCompletionResponse,
        )

    @typing_extensions.deprecated("deprecated")
    def generate_multimodality_completion(
        self,
        *,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        audio_duration: Optional[float] | Omit = omit,
        audio_type: Literal["tts", "music", "sfx"] | Omit = omit,
        context: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: Optional[str] | Omit = omit,
        num_images: int | Omit = omit,
        output_type: Literal["text", "audio", "image"] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        question: Optional[str] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        speed: float | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        voice: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGenerateMultimodalityCompletionResponse:
        """
        **DEPRECATED** — Use the new dedicated endpoints instead: - Text →
        `POST /v1/text/generations` - Image → `POST /v1/images/generations` - Audio →
        `POST /v1/audio/generations` - All → `POST /v1/chat/completions`

            This endpoint is kept for backward compatibility and internally delegates to
            the appropriate new generation handler based on `output_type`.

        Args:
          user_id: Unique identifier for the user (always required)

          audio_base64: Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)

          audio_duration: Duration in seconds for music/sfx generation. Default: 5s for sfx, 10s for music

          audio_type: Type of audio output: 'tts' for text-to-speech, 'music' for AI music, 'sfx' for
              sound effects

          context: Additional context for the question

          disabled_learning: Whether to disable learning/ingestion of the multimodal content

          image_base64: Base64 encoded image content

          max_reasoning_iterations: Maximum repair iterations in reasoning loop

          model: LLM model to use for generating the response

          num_images: Number of images to generate (each with a different seed for variation). Only
              used when output_type='image'

          output_type: Output type: 'text' for text only, 'audio' for TTS audio, 'image' for
              AI-generated image

          persona_id: Optional persona ID. If provided, inference uses this persona's context instead
              of the user

          project_id: Optional project ID. If provided, inference uses project context (inherits from
              user)

          question: User's question or prompt (optional if audio provided)

          seed: Base seed for reproducible image generation. If not provided, a random seed is
              used. Only used when output_type='image'

          session_id: Optional session identifier for conversation context

          speed: Speed of the speech (0.25 to 4.0). Only used when audio_type='tts'

          use_reasoning: Use creative reasoning loop for constraint-satisfying generation (only for
              creative_design projects with output_type='image')

          video_base64: Base64 encoded video content

          voice: Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer). Only used when
              audio_type='tts'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/inference/multimodality-completion",
            body=maybe_transform(
                {
                    "user_id": user_id,
                    "audio_base64": audio_base64,
                    "audio_duration": audio_duration,
                    "audio_type": audio_type,
                    "context": context,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "num_images": num_images,
                    "output_type": output_type,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "question": question,
                    "seed": seed,
                    "session_id": session_id,
                    "speed": speed,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                    "voice": voice,
                },
                inference_generate_multimodality_completion_params.InferenceGenerateMultimodalityCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGenerateMultimodalityCompletionResponse,
        )


class AsyncInferenceResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncInferenceResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncInferenceResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncInferenceResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncInferenceResourceWithStreamingResponse(self)

    @typing_extensions.deprecated("deprecated")
    async def generate_completion(
        self,
        *,
        content: Union[str, Iterable[Dict[str, str]]],
        user_id: str,
        disabled_learning: bool | Omit = omit,
        model: str | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGenerateCompletionResponse:
        """
        **⚠️ DEPRECATED** — Use `POST /v1/chat/completions` or
        `POST /v1/text/generations` instead.

            This endpoint is kept for backward compatibility and internally delegates to
            the new text generation handler.

        Args:
          content: Content to process

          user_id: User ID (always required)

          disabled_learning: Whether to disable learning

          model: LLM model to use for generation

          persona_id: Optional persona ID. If provided, inference uses this persona's context instead
              of the user

          project_id: Optional project ID. If provided, inference uses project context (inherits from
              user)

          session_id: Session ID

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/inference/completion",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "user_id": user_id,
                    "disabled_learning": disabled_learning,
                    "model": model,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "session_id": session_id,
                },
                inference_generate_completion_params.InferenceGenerateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGenerateCompletionResponse,
        )

    @typing_extensions.deprecated("deprecated")
    async def generate_multimodality_completion(
        self,
        *,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        audio_duration: Optional[float] | Omit = omit,
        audio_type: Literal["tts", "music", "sfx"] | Omit = omit,
        context: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        model: Optional[str] | Omit = omit,
        num_images: int | Omit = omit,
        output_type: Literal["text", "audio", "image"] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        question: Optional[str] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        speed: float | Omit = omit,
        use_reasoning: bool | Omit = omit,
        video_base64: Optional[str] | Omit = omit,
        voice: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGenerateMultimodalityCompletionResponse:
        """
        **DEPRECATED** — Use the new dedicated endpoints instead: - Text →
        `POST /v1/text/generations` - Image → `POST /v1/images/generations` - Audio →
        `POST /v1/audio/generations` - All → `POST /v1/chat/completions`

            This endpoint is kept for backward compatibility and internally delegates to
            the appropriate new generation handler based on `output_type`.

        Args:
          user_id: Unique identifier for the user (always required)

          audio_base64: Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)

          audio_duration: Duration in seconds for music/sfx generation. Default: 5s for sfx, 10s for music

          audio_type: Type of audio output: 'tts' for text-to-speech, 'music' for AI music, 'sfx' for
              sound effects

          context: Additional context for the question

          disabled_learning: Whether to disable learning/ingestion of the multimodal content

          image_base64: Base64 encoded image content

          max_reasoning_iterations: Maximum repair iterations in reasoning loop

          model: LLM model to use for generating the response

          num_images: Number of images to generate (each with a different seed for variation). Only
              used when output_type='image'

          output_type: Output type: 'text' for text only, 'audio' for TTS audio, 'image' for
              AI-generated image

          persona_id: Optional persona ID. If provided, inference uses this persona's context instead
              of the user

          project_id: Optional project ID. If provided, inference uses project context (inherits from
              user)

          question: User's question or prompt (optional if audio provided)

          seed: Base seed for reproducible image generation. If not provided, a random seed is
              used. Only used when output_type='image'

          session_id: Optional session identifier for conversation context

          speed: Speed of the speech (0.25 to 4.0). Only used when audio_type='tts'

          use_reasoning: Use creative reasoning loop for constraint-satisfying generation (only for
              creative_design projects with output_type='image')

          video_base64: Base64 encoded video content

          voice: Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer). Only used when
              audio_type='tts'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/inference/multimodality-completion",
            body=await async_maybe_transform(
                {
                    "user_id": user_id,
                    "audio_base64": audio_base64,
                    "audio_duration": audio_duration,
                    "audio_type": audio_type,
                    "context": context,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "model": model,
                    "num_images": num_images,
                    "output_type": output_type,
                    "persona_id": persona_id,
                    "project_id": project_id,
                    "question": question,
                    "seed": seed,
                    "session_id": session_id,
                    "speed": speed,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                    "voice": voice,
                },
                inference_generate_multimodality_completion_params.InferenceGenerateMultimodalityCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGenerateMultimodalityCompletionResponse,
        )


class InferenceResourceWithRawResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.generate_completion = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                inference.generate_completion,  # pyright: ignore[reportDeprecated],
            )
        )
        self.generate_multimodality_completion = (  # pyright: ignore[reportDeprecated]
            to_raw_response_wrapper(
                inference.generate_multimodality_completion,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncInferenceResourceWithRawResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.generate_completion = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                inference.generate_completion,  # pyright: ignore[reportDeprecated],
            )
        )
        self.generate_multimodality_completion = (  # pyright: ignore[reportDeprecated]
            async_to_raw_response_wrapper(
                inference.generate_multimodality_completion,  # pyright: ignore[reportDeprecated],
            )
        )


class InferenceResourceWithStreamingResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.generate_completion = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                inference.generate_completion,  # pyright: ignore[reportDeprecated],
            )
        )
        self.generate_multimodality_completion = (  # pyright: ignore[reportDeprecated]
            to_streamed_response_wrapper(
                inference.generate_multimodality_completion,  # pyright: ignore[reportDeprecated],
            )
        )


class AsyncInferenceResourceWithStreamingResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.generate_completion = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                inference.generate_completion,  # pyright: ignore[reportDeprecated],
            )
        )
        self.generate_multimodality_completion = (  # pyright: ignore[reportDeprecated]
            async_to_streamed_response_wrapper(
                inference.generate_multimodality_completion,  # pyright: ignore[reportDeprecated],
            )
        )
