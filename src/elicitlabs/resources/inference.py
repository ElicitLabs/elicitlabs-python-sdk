# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal

import httpx

from ..types import (
    inference_generate_completion_params,
    inference_generate_persona_chat_params,
    inference_generate_multimodality_completion_params,
)
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
from ..types.inference_generate_persona_chat_response import InferenceGeneratePersonaChatResponse
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

    def generate_completion(
        self,
        *,
        content: Union[str, Iterable[Dict[str, str]]],
        user_id: str,
        disabled_learning: bool | Omit = omit,
        model: str | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGenerateCompletionResponse:
        """
        Generate personalized AI completion using the Elicit Labs Modal System.

            This endpoint:
            - Takes raw messages or user query
            - Retrieves relevant memories and personalizes the context
            - Generates personalized AI response using the specified LLM model
            - Optionally learns from the conversation (disabled_learning=False)
            - Returns formatted messages with AI response

            **Authentication**: Requires valid API key or JWT token in Authorization header

        Args:
          content: Content to process

          user_id: User ID

          disabled_learning: Whether to disable learning

          model: LLM model to use for generation

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
                    "session_id": session_id,
                },
                inference_generate_completion_params.InferenceGenerateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGenerateCompletionResponse,
        )

    def generate_multimodality_completion(
        self,
        *,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        context: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        model: Optional[str] | Omit = omit,
        output_type: Literal["text", "audio", "image"] | Omit = omit,
        question: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        speed: float | Omit = omit,
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
        Generate an AI response using multimodal memory retrieval with flexible output
        types.

            This endpoint:
            1. Accepts multimodal inputs (video, image, audio) - same as multimodal-query
            2. Processes the multimodal input to extract faces, voices, and transcripts
            3. Retrieves relevant memories based on matched identities and transcripts
            4. Generates an LLM response using the memory context and multimodal data
            5. Based on output_type: returns text only, converts to speech (TTS), or generates an image
            6. Returns text response, audio/image (based on output_type), and memory context

            **Request Parameters:**
            - user_id (str, required): User or persona ID
            - question (str, optional): User's question or prompt (can be extracted from audio if not provided)
            - context (str, optional): Additional context for the question
            - session_id (str, optional): Session identifier for conversation context
            - video_base64 (str, optional): Base64 encoded video content
            - image_base64 (str, optional): Base64 encoded image content
            - audio_base64 (str, optional): Base64 encoded audio content (supports webm, wav, mp3, etc.)
            - voice (str, optional): Voice to use for TTS - options: alloy (default), echo, fable, onyx, nova, shimmer
            - speed (float, optional): Speech speed from 0.25 to 4.0 (default: 1.0)
            - model (str, optional): LLM model to use (defaults to gemini-2.5-flash)
            - output_type (str, optional): Output type - 'text' (default), 'audio' (TTS), or 'image' (AI-generated)
            - disabled_learning (bool, optional): Whether to disable ingestion/learning from the content (default: false)

            **Note:** At least one multimodal input (video, image, or audio) is required for memory retrieval.
            When disabled_learning is false, the multimodal content will also be ingested for future memory retrieval.

            **Response:**
            - text_response (str): Generated text response from the LLM
            - audio_base64 (str, optional): Base64 encoded audio (MP3 format) if output_type='audio'
            - audio_format (str, optional): Format of the audio
            - voice_used (str, optional): Voice used for TTS
            - image_base64 (str, optional): Representative image from input
            - generated_image_base64 (str, optional): AI-generated image if output_type='image'
            - memory_context (str, optional): Formatted memory context used for generation
            - raw_results (dict, optional): Raw results from memory retrieval
            - success (bool): True if request succeeded

            **Example:**
            ```json
            {
                "user_id": "user-123",
                "question": "What do you see?",
                "video_base64": "base64_encoded_video...",
                "voice": "alloy",
                "speed": 1.0,
                "model": "gemini-2.5-flash",
                "output_type": "audio",
                "disabled_learning": false
            }
            ```

            Returns 200 OK with text, audio/image (based on output_type), and memory context. Requires JWT authentication.

        Args:
          user_id: Unique identifier for the user

          audio_base64: Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)

          context: Additional context for the question

          disabled_learning: Whether to disable learning/ingestion of the multimodal content

          image_base64: Base64 encoded image content

          model: LLM model to use for generating the response

          output_type: Output type: 'text' for text only, 'audio' for TTS audio, 'image' for
              AI-generated image

          question: User's question or prompt (optional if audio provided)

          session_id: Optional session identifier for conversation context

          speed: Speed of the speech (0.25 to 4.0)

          video_base64: Base64 encoded video content

          voice: Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer)

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
                    "context": context,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "model": model,
                    "output_type": output_type,
                    "question": question,
                    "session_id": session_id,
                    "speed": speed,
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

    def generate_persona_chat(
        self,
        *,
        content: Union[str, Iterable[Dict[str, str]]],
        user_id: str,
        disabled_learning: bool | Omit = omit,
        model: str | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGeneratePersonaChatResponse:
        """
        Generate AI response as a specific persona with Elicit Labs Modal System.

            This endpoint:
            - Retrieves persona information and characteristics
            - Formats messages with persona-specific context and memories
            - Generates response in the persona's unique style and voice
            - Optionally learns from the conversation (disabled_learning=False)
            - Returns synchronous response with formatted messages

            **Authentication**: Requires valid API key or JWT token in Authorization header

        Args:
          content: Content to process

          user_id: User ID (persona ID)

          disabled_learning: Whether to disable learning

          model: LLM model to use for generation

          session_id: Session identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/inference/persona-chat",
            body=maybe_transform(
                {
                    "content": content,
                    "user_id": user_id,
                    "disabled_learning": disabled_learning,
                    "model": model,
                    "session_id": session_id,
                },
                inference_generate_persona_chat_params.InferenceGeneratePersonaChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGeneratePersonaChatResponse,
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

    async def generate_completion(
        self,
        *,
        content: Union[str, Iterable[Dict[str, str]]],
        user_id: str,
        disabled_learning: bool | Omit = omit,
        model: str | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGenerateCompletionResponse:
        """
        Generate personalized AI completion using the Elicit Labs Modal System.

            This endpoint:
            - Takes raw messages or user query
            - Retrieves relevant memories and personalizes the context
            - Generates personalized AI response using the specified LLM model
            - Optionally learns from the conversation (disabled_learning=False)
            - Returns formatted messages with AI response

            **Authentication**: Requires valid API key or JWT token in Authorization header

        Args:
          content: Content to process

          user_id: User ID

          disabled_learning: Whether to disable learning

          model: LLM model to use for generation

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
                    "session_id": session_id,
                },
                inference_generate_completion_params.InferenceGenerateCompletionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGenerateCompletionResponse,
        )

    async def generate_multimodality_completion(
        self,
        *,
        user_id: str,
        audio_base64: Optional[str] | Omit = omit,
        context: Optional[str] | Omit = omit,
        disabled_learning: bool | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        model: Optional[str] | Omit = omit,
        output_type: Literal["text", "audio", "image"] | Omit = omit,
        question: Optional[str] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        speed: float | Omit = omit,
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
        Generate an AI response using multimodal memory retrieval with flexible output
        types.

            This endpoint:
            1. Accepts multimodal inputs (video, image, audio) - same as multimodal-query
            2. Processes the multimodal input to extract faces, voices, and transcripts
            3. Retrieves relevant memories based on matched identities and transcripts
            4. Generates an LLM response using the memory context and multimodal data
            5. Based on output_type: returns text only, converts to speech (TTS), or generates an image
            6. Returns text response, audio/image (based on output_type), and memory context

            **Request Parameters:**
            - user_id (str, required): User or persona ID
            - question (str, optional): User's question or prompt (can be extracted from audio if not provided)
            - context (str, optional): Additional context for the question
            - session_id (str, optional): Session identifier for conversation context
            - video_base64 (str, optional): Base64 encoded video content
            - image_base64 (str, optional): Base64 encoded image content
            - audio_base64 (str, optional): Base64 encoded audio content (supports webm, wav, mp3, etc.)
            - voice (str, optional): Voice to use for TTS - options: alloy (default), echo, fable, onyx, nova, shimmer
            - speed (float, optional): Speech speed from 0.25 to 4.0 (default: 1.0)
            - model (str, optional): LLM model to use (defaults to gemini-2.5-flash)
            - output_type (str, optional): Output type - 'text' (default), 'audio' (TTS), or 'image' (AI-generated)
            - disabled_learning (bool, optional): Whether to disable ingestion/learning from the content (default: false)

            **Note:** At least one multimodal input (video, image, or audio) is required for memory retrieval.
            When disabled_learning is false, the multimodal content will also be ingested for future memory retrieval.

            **Response:**
            - text_response (str): Generated text response from the LLM
            - audio_base64 (str, optional): Base64 encoded audio (MP3 format) if output_type='audio'
            - audio_format (str, optional): Format of the audio
            - voice_used (str, optional): Voice used for TTS
            - image_base64 (str, optional): Representative image from input
            - generated_image_base64 (str, optional): AI-generated image if output_type='image'
            - memory_context (str, optional): Formatted memory context used for generation
            - raw_results (dict, optional): Raw results from memory retrieval
            - success (bool): True if request succeeded

            **Example:**
            ```json
            {
                "user_id": "user-123",
                "question": "What do you see?",
                "video_base64": "base64_encoded_video...",
                "voice": "alloy",
                "speed": 1.0,
                "model": "gemini-2.5-flash",
                "output_type": "audio",
                "disabled_learning": false
            }
            ```

            Returns 200 OK with text, audio/image (based on output_type), and memory context. Requires JWT authentication.

        Args:
          user_id: Unique identifier for the user

          audio_base64: Base64 encoded audio content (supports webm, wav, mp3, mp4, and other formats)

          context: Additional context for the question

          disabled_learning: Whether to disable learning/ingestion of the multimodal content

          image_base64: Base64 encoded image content

          model: LLM model to use for generating the response

          output_type: Output type: 'text' for text only, 'audio' for TTS audio, 'image' for
              AI-generated image

          question: User's question or prompt (optional if audio provided)

          session_id: Optional session identifier for conversation context

          speed: Speed of the speech (0.25 to 4.0)

          video_base64: Base64 encoded video content

          voice: Voice to use for TTS (alloy, echo, fable, onyx, nova, shimmer)

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
                    "context": context,
                    "disabled_learning": disabled_learning,
                    "image_base64": image_base64,
                    "model": model,
                    "output_type": output_type,
                    "question": question,
                    "session_id": session_id,
                    "speed": speed,
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

    async def generate_persona_chat(
        self,
        *,
        content: Union[str, Iterable[Dict[str, str]]],
        user_id: str,
        disabled_learning: bool | Omit = omit,
        model: str | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> InferenceGeneratePersonaChatResponse:
        """
        Generate AI response as a specific persona with Elicit Labs Modal System.

            This endpoint:
            - Retrieves persona information and characteristics
            - Formats messages with persona-specific context and memories
            - Generates response in the persona's unique style and voice
            - Optionally learns from the conversation (disabled_learning=False)
            - Returns synchronous response with formatted messages

            **Authentication**: Requires valid API key or JWT token in Authorization header

        Args:
          content: Content to process

          user_id: User ID (persona ID)

          disabled_learning: Whether to disable learning

          model: LLM model to use for generation

          session_id: Session identifier

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/inference/persona-chat",
            body=await async_maybe_transform(
                {
                    "content": content,
                    "user_id": user_id,
                    "disabled_learning": disabled_learning,
                    "model": model,
                    "session_id": session_id,
                },
                inference_generate_persona_chat_params.InferenceGeneratePersonaChatParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=InferenceGeneratePersonaChatResponse,
        )


class InferenceResourceWithRawResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.generate_completion = to_raw_response_wrapper(
            inference.generate_completion,
        )
        self.generate_multimodality_completion = to_raw_response_wrapper(
            inference.generate_multimodality_completion,
        )
        self.generate_persona_chat = to_raw_response_wrapper(
            inference.generate_persona_chat,
        )


class AsyncInferenceResourceWithRawResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.generate_completion = async_to_raw_response_wrapper(
            inference.generate_completion,
        )
        self.generate_multimodality_completion = async_to_raw_response_wrapper(
            inference.generate_multimodality_completion,
        )
        self.generate_persona_chat = async_to_raw_response_wrapper(
            inference.generate_persona_chat,
        )


class InferenceResourceWithStreamingResponse:
    def __init__(self, inference: InferenceResource) -> None:
        self._inference = inference

        self.generate_completion = to_streamed_response_wrapper(
            inference.generate_completion,
        )
        self.generate_multimodality_completion = to_streamed_response_wrapper(
            inference.generate_multimodality_completion,
        )
        self.generate_persona_chat = to_streamed_response_wrapper(
            inference.generate_persona_chat,
        )


class AsyncInferenceResourceWithStreamingResponse:
    def __init__(self, inference: AsyncInferenceResource) -> None:
        self._inference = inference

        self.generate_completion = async_to_streamed_response_wrapper(
            inference.generate_completion,
        )
        self.generate_multimodality_completion = async_to_streamed_response_wrapper(
            inference.generate_multimodality_completion,
        )
        self.generate_persona_chat = async_to_streamed_response_wrapper(
            inference.generate_persona_chat,
        )
