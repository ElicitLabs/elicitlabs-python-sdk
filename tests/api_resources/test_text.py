# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import TextGenerateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestText:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate(self, client: ElicitClient) -> None:
        text = client.text.generate(
            user_id="user_123",
        )
        assert_matches_type(TextGenerateResponse, text, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_with_all_params(self, client: ElicitClient) -> None:
        text = client.text.generate(
            user_id="user_123",
            audio_base64="audio_base64",
            disabled_learning=True,
            image_base64="image_base64",
            max_reasoning_iterations=1,
            model="gpt-4.1-mini",
            output_schema={"foo": "bar"},
            persona_id="persona_id",
            project_id="proj_ABC",
            session_id="session_id",
            text_input="Write a blog post about AI",
            use_reasoning=False,
            video_base64="video_base64",
        )
        assert_matches_type(TextGenerateResponse, text, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_generate(self, client: ElicitClient) -> None:
        response = client.text.with_raw_response.generate(
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        text = response.parse()
        assert_matches_type(TextGenerateResponse, text, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_generate(self, client: ElicitClient) -> None:
        with client.text.with_streaming_response.generate(
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            text = response.parse()
            assert_matches_type(TextGenerateResponse, text, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncText:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate(self, async_client: AsyncElicitClient) -> None:
        text = await async_client.text.generate(
            user_id="user_123",
        )
        assert_matches_type(TextGenerateResponse, text, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_with_all_params(self, async_client: AsyncElicitClient) -> None:
        text = await async_client.text.generate(
            user_id="user_123",
            audio_base64="audio_base64",
            disabled_learning=True,
            image_base64="image_base64",
            max_reasoning_iterations=1,
            model="gpt-4.1-mini",
            output_schema={"foo": "bar"},
            persona_id="persona_id",
            project_id="proj_ABC",
            session_id="session_id",
            text_input="Write a blog post about AI",
            use_reasoning=False,
            video_base64="video_base64",
        )
        assert_matches_type(TextGenerateResponse, text, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_generate(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.text.with_raw_response.generate(
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        text = await response.parse()
        assert_matches_type(TextGenerateResponse, text, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_generate(self, async_client: AsyncElicitClient) -> None:
        async with async_client.text.with_streaming_response.generate(
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            text = await response.parse()
            assert_matches_type(TextGenerateResponse, text, path=["response"])

        assert cast(Any, response.is_closed) is True
