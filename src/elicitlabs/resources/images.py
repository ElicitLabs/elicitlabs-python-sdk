# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

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
        aspect_ratio: str | Omit = omit,
        edit: Optional[image_generate_params.Edit] | Omit = omit,
        make_editable: Optional[bool] | Omit = omit,
        mode: Optional[Literal["default", "consistency", "exploration", "edit", "relayout"]] | Omit = omit,
        model: str | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        relayout: Optional[image_generate_params.Relayout] | Omit = omit,
        resolution: Literal["1K", "2K", "4K"] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ImageGenerateResponse:
        """Queues an image generation job.

        Returns `{job_id, generation_id}` — poll
        `/v1/data/job/status` with the job_id, then fetch the final image via
        `/v1/images/generations/{generation_id}/...`. See the request model for
        per-field documentation.

        Args:
          text_input: The prompt / change instruction

          user_id: The end-user ID

          aspect_ratio: Aspect ratio, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'.

          edit: Options accepted only when `mode='edit'`.

          make_editable: When true, intermediate artifacts (raw Gemini base, overlay HTML) are retained
              so the result can be re-edited. Applies to consistency and relayout modes.
              Defaults to true.

          mode: None / 'default' / 'consistency': wireframer → typesetter → synthesizer →
              refiner pipeline that reproduces stored entities/assets faithfully.
              'exploration': creative-freedom path (NOT YET IMPLEMENTED — ships this weekend).
              'edit': edit a prior generation — requires `edit` options. 'relayout': recreate
              a successful-example ad — requires `relayout` options.

          model: Image generation model ID

          project_id: The project ID

          relayout: Options accepted only when `mode='relayout'`.

          resolution: Resolution tier.

          seed: Random seed for reproducibility

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
                    "edit": edit,
                    "make_editable": make_editable,
                    "mode": mode,
                    "model": model,
                    "project_id": project_id,
                    "relayout": relayout,
                    "resolution": resolution,
                    "seed": seed,
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
        edit: Optional[image_generate_params.Edit] | Omit = omit,
        make_editable: Optional[bool] | Omit = omit,
        mode: Optional[Literal["default", "consistency", "exploration", "edit", "relayout"]] | Omit = omit,
        model: str | Omit = omit,
        project_id: Optional[str] | Omit = omit,
        relayout: Optional[image_generate_params.Relayout] | Omit = omit,
        resolution: Literal["1K", "2K", "4K"] | Omit = omit,
        seed: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ImageGenerateResponse:
        """Queues an image generation job.

        Returns `{job_id, generation_id}` — poll
        `/v1/data/job/status` with the job_id, then fetch the final image via
        `/v1/images/generations/{generation_id}/...`. See the request model for
        per-field documentation.

        Args:
          text_input: The prompt / change instruction

          user_id: The end-user ID

          aspect_ratio: Aspect ratio, e.g. '1:1', '16:9', '9:16', '4:3', '3:4'.

          edit: Options accepted only when `mode='edit'`.

          make_editable: When true, intermediate artifacts (raw Gemini base, overlay HTML) are retained
              so the result can be re-edited. Applies to consistency and relayout modes.
              Defaults to true.

          mode: None / 'default' / 'consistency': wireframer → typesetter → synthesizer →
              refiner pipeline that reproduces stored entities/assets faithfully.
              'exploration': creative-freedom path (NOT YET IMPLEMENTED — ships this weekend).
              'edit': edit a prior generation — requires `edit` options. 'relayout': recreate
              a successful-example ad — requires `relayout` options.

          model: Image generation model ID

          project_id: The project ID

          relayout: Options accepted only when `mode='relayout'`.

          resolution: Resolution tier.

          seed: Random seed for reproducibility

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
                    "edit": edit,
                    "make_editable": make_editable,
                    "mode": mode,
                    "model": model,
                    "project_id": project_id,
                    "relayout": relayout,
                    "resolution": resolution,
                    "seed": seed,
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
