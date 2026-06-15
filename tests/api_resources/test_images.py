# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import ImageGenerateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestImages:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate(self, client: ElicitClient) -> None:
        image = client.images.generate(
            text_input="text_input",
            user_id="user_id",
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_with_all_params(self, client: ElicitClient) -> None:
        image = client.images.generate(
            text_input="text_input",
            user_id="user_id",
            aspect_ratio="aspect_ratio",
            edit={"source_generation_id": "source_generation_id"},
            make_editable=True,
            mode="default",
            model="model",
            project_id="project_id",
            relayout={
                "ad_id": "ad_id",
                "target_aspect_ratios": ["string"],
            },
            resolution="1K",
            seed=0,
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_generate(self, client: ElicitClient) -> None:
        response = client.images.with_raw_response.generate(
            text_input="text_input",
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = response.parse()
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_generate(self, client: ElicitClient) -> None:
        with client.images.with_streaming_response.generate(
            text_input="text_input",
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = response.parse()
            assert_matches_type(ImageGenerateResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncImages:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate(self, async_client: AsyncElicitClient) -> None:
        image = await async_client.images.generate(
            text_input="text_input",
            user_id="user_id",
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_with_all_params(self, async_client: AsyncElicitClient) -> None:
        image = await async_client.images.generate(
            text_input="text_input",
            user_id="user_id",
            aspect_ratio="aspect_ratio",
            edit={"source_generation_id": "source_generation_id"},
            make_editable=True,
            mode="default",
            model="model",
            project_id="project_id",
            relayout={
                "ad_id": "ad_id",
                "target_aspect_ratios": ["string"],
            },
            resolution="1K",
            seed=0,
        )
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_generate(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.images.with_raw_response.generate(
            text_input="text_input",
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        image = await response.parse()
        assert_matches_type(ImageGenerateResponse, image, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_generate(self, async_client: AsyncElicitClient) -> None:
        async with async_client.images.with_streaming_response.generate(
            text_input="text_input",
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            image = await response.parse()
            assert_matches_type(ImageGenerateResponse, image, path=["response"])

        assert cast(Any, response.is_closed) is True
