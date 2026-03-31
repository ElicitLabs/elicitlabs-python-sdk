# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional, Union
from typing_extensions import Literal

import httpx

from ..types import audio_generate_params
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
from ..types.audio_generate_response import AudioGenerateResponse
from ..types.async_generation_response import AsyncGenerationResponse

__all__ = ["AudioResource", "AsyncAudioResource"]


class AudioResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AudioResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AudioResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AudioResourceWithStreamingResponse(self)

    def generate(
        self,
        *,
        text_input: str,
        user_id: str,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        audio_type: Literal["speech", "sfx", "music"] | Omit = omit,
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
    ) -> Union[AudioGenerateResponse, AsyncGenerationResponse]:
        """
        Dedicated audio generation endpoint using the Universal Schema with flat
        parameters.

            Supports three audio types:
            - **speech**: Multi-speaker TTS (auto-detects characters, designs unique voices per entity)
            - **music**: AI-generated music
            - **sfx**: AI-generated sound effects

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, required): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory

            **Input:**
            - text_input (str, required): Text to speak or audio prompt
            - context (str, optional): Additional context

            **Audio Params (Flat):**
            - model (str, required): Model ID (e.g., eleven-turbo)
            - voice (str, required): Voice ID for TTS
            - audio_type (str, optional): 'speech', 'music', or 'sfx'
            - speed (float, optional): Playback speed (0.5-2.0)
            - duration (float, optional): Max duration in seconds
            - seed (int, optional): Random seed for reproducibility

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Authentication**: Requires valid API key or JWT token

            Note: Reasoning is not currently supported for audio generation.

        Args:
          text_input: The prompt/description for audio generation

          user_id: The end-user ID

          audio_base64: Base64 encoded reference audio for context

          audio_type: Audio type: 'speech', 'sfx', or 'music'

          disabled_learning: If true, this request is ignored by long-term memory

          duration: Max duration in seconds for music/sfx (Lyria 2 always generates 30s)

          image_base64: Base64 encoded reference image for context

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: Audio generation model: 'lyria-2' (Google Lyria 2 on Vertex AI, default for
              music — 30s 48kHz WAV), 'audiocraft' (MusicGen/AudioGen on Cloud Run), or
              'eleven-turbo' (ElevenLabs TTS for speech)

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          seed: Random seed for deterministic generation (Lyria 2 only, cannot be combined with
              sample_count)

          session_id: Session ID for conversation context

          speed: Playback speed (0.5-2.0), only for speech

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before answering

          video_base64: Base64 encoded reference video for context

          voice: Voice ID for TTS (alloy, echo, fable, onyx, nova, shimmer)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/audio/generations",
            body=maybe_transform(
                {
                    "text_input": text_input,
                    "user_id": user_id,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "audio_type": audio_type,
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
                    "speed": speed,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                    "voice": voice,
                },
                audio_generate_params.AudioGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AudioGenerateResponse,
        )


class AsyncAudioResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAudioResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncAudioResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAudioResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncAudioResourceWithStreamingResponse(self)

    async def generate(
        self,
        *,
        text_input: str,
        user_id: str,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        audio_type: Literal["speech", "sfx", "music"] | Omit = omit,
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
    ) -> Union[AudioGenerateResponse, AsyncGenerationResponse]:
        """
        Dedicated audio generation endpoint using the Universal Schema with flat
        parameters.

            Supports three audio types:
            - **speech**: Multi-speaker TTS (auto-detects characters, designs unique voices per entity)
            - **music**: AI-generated music
            - **sfx**: AI-generated sound effects

            **Universal Base Schema:**
            - user_id (str, required): The end-user ID
            - project_id (str, required): The project ID
            - persona_id (str, optional): The specific system persona/voice to use
            - disabled_learning (bool, optional): If true, request is ignored by long-term memory

            **Input:**
            - text_input (str, required): Text to speak or audio prompt
            - context (str, optional): Additional context

            **Audio Params (Flat):**
            - model (str, required): Model ID (e.g., eleven-turbo)
            - voice (str, required): Voice ID for TTS
            - audio_type (str, optional): 'speech', 'music', or 'sfx'
            - speed (float, optional): Playback speed (0.5-2.0)
            - duration (float, optional): Max duration in seconds
            - seed (int, optional): Random seed for reproducibility

            **Reference inputs:**
            - image_base64 (str, optional): Base64 encoded reference image for context
            - video_base64 (str, optional): Base64 encoded reference video for context
            - audio_base64 (str, optional): Base64 encoded reference audio for context

            **Authentication**: Requires valid API key or JWT token

            Note: Reasoning is not currently supported for audio generation.

        Args:
          text_input: The prompt/description for audio generation

          user_id: The end-user ID

          audio_base64: Base64 encoded reference audio for context

          audio_type: Audio type: 'speech', 'sfx', or 'music'

          disabled_learning: If true, this request is ignored by long-term memory

          duration: Max duration in seconds for music/sfx (Lyria 2 always generates 30s)

          image_base64: Base64 encoded reference image for context

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          model: Audio generation model: 'lyria-2' (Google Lyria 2 on Vertex AI, default for
              music — 30s 48kHz WAV), 'audiocraft' (MusicGen/AudioGen on Cloud Run), or
              'eleven-turbo' (ElevenLabs TTS for speech)

          persona_id: The specific system persona/voice to use

          project_id: The project ID

          seed: Random seed for deterministic generation (Lyria 2 only, cannot be combined with
              sample_count)

          session_id: Session ID for conversation context

          speed: Playback speed (0.5-2.0), only for speech

          use_reasoning: Enable Chain-of-Thought/Reasoning steps before answering

          video_base64: Base64 encoded reference video for context

          voice: Voice ID for TTS (alloy, echo, fable, onyx, nova, shimmer)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/audio/generations",
            body=await async_maybe_transform(
                {
                    "text_input": text_input,
                    "user_id": user_id,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "audio_type": audio_type,
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
                    "speed": speed,
                    "use_reasoning": use_reasoning,
                    "video_base64": video_base64,
                    "voice": voice,
                },
                audio_generate_params.AudioGenerateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AudioGenerateResponse,
        )


class AudioResourceWithRawResponse:
    def __init__(self, audio: AudioResource) -> None:
        self._audio = audio

        self.generate = to_raw_response_wrapper(
            audio.generate,
        )


class AsyncAudioResourceWithRawResponse:
    def __init__(self, audio: AsyncAudioResource) -> None:
        self._audio = audio

        self.generate = async_to_raw_response_wrapper(
            audio.generate,
        )


class AudioResourceWithStreamingResponse:
    def __init__(self, audio: AudioResource) -> None:
        self._audio = audio

        self.generate = to_streamed_response_wrapper(
            audio.generate,
        )


class AsyncAudioResourceWithStreamingResponse:
    def __init__(self, audio: AsyncAudioResource) -> None:
        self._audio = audio

        self.generate = async_to_streamed_response_wrapper(
            audio.generate,
        )
