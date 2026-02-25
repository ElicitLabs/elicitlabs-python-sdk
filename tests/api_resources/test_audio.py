# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import AudioGenerateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAudio:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate(self, client: ElicitClient) -> None:
        audio = client.audio.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
        )
        assert_matches_type(AudioGenerateResponse, audio, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_with_all_params(self, client: ElicitClient) -> None:
        audio = client.audio.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
            audio_base64="audio_base64",
            audio_type="speech",
            disabled_learning=True,
            duration=0,
            image_base64="image_base64",
            model="eleven-turbo",
            persona_id="persona_id",
            project_id="proj_ABC",
            seed=0,
            session_id="session_id",
            speed=1,
            video_base64="video_base64",
            voice="rachel",
        )
        assert_matches_type(AudioGenerateResponse, audio, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_generate(self, client: ElicitClient) -> None:
        response = client.audio.with_raw_response.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audio = response.parse()
        assert_matches_type(AudioGenerateResponse, audio, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_generate(self, client: ElicitClient) -> None:
        with client.audio.with_streaming_response.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audio = response.parse()
            assert_matches_type(AudioGenerateResponse, audio, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAudio:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate(self, async_client: AsyncElicitClient) -> None:
        audio = await async_client.audio.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
        )
        assert_matches_type(AudioGenerateResponse, audio, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_with_all_params(self, async_client: AsyncElicitClient) -> None:
        audio = await async_client.audio.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
            audio_base64="audio_base64",
            audio_type="speech",
            disabled_learning=True,
            duration=0,
            image_base64="image_base64",
            model="eleven-turbo",
            persona_id="persona_id",
            project_id="proj_ABC",
            seed=0,
            session_id="session_id",
            speed=1,
            video_base64="video_base64",
            voice="rachel",
        )
        assert_matches_type(AudioGenerateResponse, audio, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_generate(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.audio.with_raw_response.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        audio = await response.parse()
        assert_matches_type(AudioGenerateResponse, audio, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_generate(self, async_client: AsyncElicitClient) -> None:
        async with async_client.audio.with_streaming_response.generate(
            text_input="Hello world, this is a test.",
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            audio = await response.parse()
            assert_matches_type(AudioGenerateResponse, audio, path=["response"])

        assert cast(Any, response.is_closed) is True
