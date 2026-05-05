# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..types import image_generate_params
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
        aspect_ratio: str | Omit = omit,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        callback_url: Optional[str] | Omit = omit,
        debug: bool | Omit = omit,
        disabled_learning: bool | Omit = omit,
        font_reference_image_base64: Optional[SequenceNotStr[str]] | Omit = omit,
        font_reference_image_url: Optional[SequenceNotStr[str]] | Omit = omit,
        font_reference_ttf_base64: Optional[SequenceNotStr[str]] | Omit = omit,
        font_reference_ttf_url: Optional[SequenceNotStr[str]] | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        mask_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        mode: Optional[Literal["fast", "default", "consistency", "exploration", "edit"]] | Omit = omit,
        model: str | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        pinned_entity_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        pinned_folder_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        resolution: Literal["1K", "2K", "4K"] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        source_generation_id: Optional[str] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
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
            - model (str, optional): Model ID (default: gemini-3.1-flash). Available models: gemini-3.1-flash, gemini-3-flash, gemini-3.1-pro, gpt-image-1, gpt-image-1.5, gpt-image-2, flux-2-max, flux-2-pro, flux-2-klein-9b, flux-2-schnell, flux-pro-1.1, flux-pro-1.1-ultra, flux-kontext-pro, imagen-4-fast, imagen-4-ultra
            - aspect_ratio (str, optional): Aspect ratio, e.g. "1:1", "16:9", "9:16" (default: 1:1).
            - resolution (str, optional): Resolution tier: "1K", "2K", or "4K" (default: 4K).
            - seed (int, optional): Random seed for reproducibility

            **Authentication**: Requires valid API key or JWT token

        Args:
          text_input: The prompt/description for image generation

          user_id: The end-user ID

          aspect_ratio: Aspect ratio for the generated image, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'.

          async_mode: If true, return a job_id immediately and process in the background

          audio_base64: Base64 encoded reference audio for context

          callback_url: Optional URL the server will POST to when generation completes.

          debug: If true, capture a self-contained HTML trace of every pipeline step (retrieval
              LLM calls, synthesis, prompt assembly, image LLM, post-gen text fix, edit-text
              refinement loop) to data/temp/<ts>\\__pipeline_trace.html. Also activates
              automatically when the server is started with the `DEBUG` environment variable
              set to a truthy value (true/1/yes).

          disabled_learning: If true, this request is ignored by long-term memory

          font_reference_image_base64: List of base64-encoded PNG/JPG images showing the desired font (e.g., a
              typography specimen). Honored only when mode='edit'.

          font_reference_image_url: List of HTTPS or gs:// URLs to images showing the desired font. Server downloads
              them. Honored only when mode='edit'.

          font_reference_ttf_base64: List of base64-encoded TTF/OTF font file bytes (drag-and-drop support — no
              upload endpoint required). The server decodes, renders a typography sample, and
              passes the rendered image as a reference. Honored only when mode='edit'.

          font_reference_ttf_url: List of HTTPS or gs:// URLs to TTF/OTF font files. The server renders a
              typography sample in each font and passes the rendered image as a reference.
              Honored only when mode='edit'.

          image_base64: Base64 encoded reference image for context

          mask_base64: Optional base64 PNG mask for inpainting (only honored on gpt-image-\\** models).
              Transparent pixels = edit region, opaque pixels = keep. Silently ignored by
              Flux/Imagen/Gemini providers.

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          mode:
              Generation mode controlling how reference assets are used. None or 'default':
              Standard pipeline — synthesis LLM picks consistency vs exploration based on the
              prompt. 'consistency': Reproduce stored entities/assets faithfully — match their
              canonical look and the project's documented details. 'exploration': Creative
              freedom — generate new content / new compositions where references guide
              aesthetic and style only, not exact appearance. The post-gen text fix is skipped
              in this mode (the model's own text rendering is trusted). 'fast': Skip
              hierarchical retrieval, single-call block selector. 'edit': Edit a prior
              generation referenced by source_generation_id; text_input is the change
              instruction. Skips memory retrieval — the source image IS the context. Legacy
              values 'faithful', 'style_transfer', 'create_new' are auto-coerced
              ('faithful'→'consistency', the other two→'exploration').

          model: Image generation model ID

          notification_email: Optional email address to notify when generation completes.

          persona_id: The specific system persona/voice to use

          pinned_entity_ids: OBJECTS entity node IDs to anchor flat memory retrieval. When set, memory
              retrieval focuses on episodes/memories connected to these specific entities
              instead of fully autonomous semantic search.

          pinned_folder_ids: HierarchicalFolder node IDs to anchor hierarchical retrieval. When set, the
              retrieval pipeline targets these folders directly instead of using LLM path
              selection.

          project_id: The project ID

          resolution: Resolution tier for the generated image: '1K', '2K', or '4K'.

          seed: Random seed for reproducibility

          session_id: Session ID for conversation context

          source_generation_id: ID of a previously generated image (row in upl.generations) to edit. Required
              when mode='edit'. The server fetches the source from GCS — no upload needed.
              Must belong to the requesting user.

          temperature: Temperature for retrieval LLM calls (0.0-2.0). Lower = more deterministic.

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
                    "aspect_ratio": aspect_ratio,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "callback_url": callback_url,
                    "debug": debug,
                    "disabled_learning": disabled_learning,
                    "font_reference_image_base64": font_reference_image_base64,
                    "font_reference_image_url": font_reference_image_url,
                    "font_reference_ttf_base64": font_reference_ttf_base64,
                    "font_reference_ttf_url": font_reference_ttf_url,
                    "image_base64": image_base64,
                    "mask_base64": mask_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "mode": mode,
                    "model": model,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "pinned_entity_ids": pinned_entity_ids,
                    "pinned_folder_ids": pinned_folder_ids,
                    "project_id": project_id,
                    "resolution": resolution,
                    "seed": seed,
                    "session_id": session_id,
                    "source_generation_id": source_generation_id,
                    "temperature": temperature,
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
        aspect_ratio: str | Omit = omit,
        async_mode: bool | Omit = omit,
        audio_base64: Optional[str] | Omit = omit,
        callback_url: Optional[str] | Omit = omit,
        debug: bool | Omit = omit,
        disabled_learning: bool | Omit = omit,
        font_reference_image_base64: Optional[SequenceNotStr[str]] | Omit = omit,
        font_reference_image_url: Optional[SequenceNotStr[str]] | Omit = omit,
        font_reference_ttf_base64: Optional[SequenceNotStr[str]] | Omit = omit,
        font_reference_ttf_url: Optional[SequenceNotStr[str]] | Omit = omit,
        image_base64: Optional[str] | Omit = omit,
        mask_base64: Optional[str] | Omit = omit,
        max_reasoning_iterations: int | Omit = omit,
        mode: Optional[Literal["fast", "default", "consistency", "exploration", "edit"]] | Omit = omit,
        model: str | Omit = omit,
        notification_email: Optional[str] | Omit = omit,
        persona_id: Optional[str] | Omit = omit,
        pinned_entity_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        pinned_folder_ids: Optional[SequenceNotStr[str]] | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        resolution: Literal["1K", "2K", "4K"] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        session_id: Optional[str] | Omit = omit,
        source_generation_id: Optional[str] | Omit = omit,
        temperature: Optional[float] | Omit = omit,
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
            - model (str, optional): Model ID (default: gemini-3.1-flash). Available models: gemini-3.1-flash, gemini-3-flash, gemini-3.1-pro, gpt-image-1, gpt-image-1.5, gpt-image-2, flux-2-max, flux-2-pro, flux-2-klein-9b, flux-2-schnell, flux-pro-1.1, flux-pro-1.1-ultra, flux-kontext-pro, imagen-4-fast, imagen-4-ultra
            - aspect_ratio (str, optional): Aspect ratio, e.g. "1:1", "16:9", "9:16" (default: 1:1).
            - resolution (str, optional): Resolution tier: "1K", "2K", or "4K" (default: 4K).
            - seed (int, optional): Random seed for reproducibility

            **Authentication**: Requires valid API key or JWT token

        Args:
          text_input: The prompt/description for image generation

          user_id: The end-user ID

          aspect_ratio: Aspect ratio for the generated image, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'.

          async_mode: If true, return a job_id immediately and process in the background

          audio_base64: Base64 encoded reference audio for context

          callback_url: Optional URL the server will POST to when generation completes.

          debug: If true, capture a self-contained HTML trace of every pipeline step (retrieval
              LLM calls, synthesis, prompt assembly, image LLM, post-gen text fix, edit-text
              refinement loop) to data/temp/<ts>\\__pipeline_trace.html. Also activates
              automatically when the server is started with the `DEBUG` environment variable
              set to a truthy value (true/1/yes).

          disabled_learning: If true, this request is ignored by long-term memory

          font_reference_image_base64: List of base64-encoded PNG/JPG images showing the desired font (e.g., a
              typography specimen). Honored only when mode='edit'.

          font_reference_image_url: List of HTTPS or gs:// URLs to images showing the desired font. Server downloads
              them. Honored only when mode='edit'.

          font_reference_ttf_base64: List of base64-encoded TTF/OTF font file bytes (drag-and-drop support — no
              upload endpoint required). The server decodes, renders a typography sample, and
              passes the rendered image as a reference. Honored only when mode='edit'.

          font_reference_ttf_url: List of HTTPS or gs:// URLs to TTF/OTF font files. The server renders a
              typography sample in each font and passes the rendered image as a reference.
              Honored only when mode='edit'.

          image_base64: Base64 encoded reference image for context

          mask_base64: Optional base64 PNG mask for inpainting (only honored on gpt-image-\\** models).
              Transparent pixels = edit region, opaque pixels = keep. Silently ignored by
              Flux/Imagen/Gemini providers.

          max_reasoning_iterations: Max reasoning steps if reasoning is enabled

          mode:
              Generation mode controlling how reference assets are used. None or 'default':
              Standard pipeline — synthesis LLM picks consistency vs exploration based on the
              prompt. 'consistency': Reproduce stored entities/assets faithfully — match their
              canonical look and the project's documented details. 'exploration': Creative
              freedom — generate new content / new compositions where references guide
              aesthetic and style only, not exact appearance. The post-gen text fix is skipped
              in this mode (the model's own text rendering is trusted). 'fast': Skip
              hierarchical retrieval, single-call block selector. 'edit': Edit a prior
              generation referenced by source_generation_id; text_input is the change
              instruction. Skips memory retrieval — the source image IS the context. Legacy
              values 'faithful', 'style_transfer', 'create_new' are auto-coerced
              ('faithful'→'consistency', the other two→'exploration').

          model: Image generation model ID

          notification_email: Optional email address to notify when generation completes.

          persona_id: The specific system persona/voice to use

          pinned_entity_ids: OBJECTS entity node IDs to anchor flat memory retrieval. When set, memory
              retrieval focuses on episodes/memories connected to these specific entities
              instead of fully autonomous semantic search.

          pinned_folder_ids: HierarchicalFolder node IDs to anchor hierarchical retrieval. When set, the
              retrieval pipeline targets these folders directly instead of using LLM path
              selection.

          project_id: The project ID

          resolution: Resolution tier for the generated image: '1K', '2K', or '4K'.

          seed: Random seed for reproducibility

          session_id: Session ID for conversation context

          source_generation_id: ID of a previously generated image (row in upl.generations) to edit. Required
              when mode='edit'. The server fetches the source from GCS — no upload needed.
              Must belong to the requesting user.

          temperature: Temperature for retrieval LLM calls (0.0-2.0). Lower = more deterministic.

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
                    "aspect_ratio": aspect_ratio,
                    "async_mode": async_mode,
                    "audio_base64": audio_base64,
                    "callback_url": callback_url,
                    "debug": debug,
                    "disabled_learning": disabled_learning,
                    "font_reference_image_base64": font_reference_image_base64,
                    "font_reference_image_url": font_reference_image_url,
                    "font_reference_ttf_base64": font_reference_ttf_base64,
                    "font_reference_ttf_url": font_reference_ttf_url,
                    "image_base64": image_base64,
                    "mask_base64": mask_base64,
                    "max_reasoning_iterations": max_reasoning_iterations,
                    "mode": mode,
                    "model": model,
                    "notification_email": notification_email,
                    "persona_id": persona_id,
                    "pinned_entity_ids": pinned_entity_ids,
                    "pinned_folder_ids": pinned_folder_ids,
                    "project_id": project_id,
                    "resolution": resolution,
                    "seed": seed,
                    "session_id": session_id,
                    "source_generation_id": source_generation_id,
                    "temperature": temperature,
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
