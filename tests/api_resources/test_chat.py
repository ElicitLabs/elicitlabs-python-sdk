# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import ChatCreateCompletionResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChat:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_completion(self, client: ElicitClient) -> None:
        chat = client.chat.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_completion_with_all_params(self, client: ElicitClient) -> None:
        chat = client.chat.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
            agent_mode=True,
            audio_config={
                "audio_type": "audio_type",
                "duration": 0,
                "model": "model",
                "speed": 0.25,
                "voice": "voice",
            },
            auto_detect_agent=True,
            disabled_learning=True,
            history_limit=1,
            image_config={
                "model": "model",
                "seed": 0,
                "size": "size",
            },
            load_history=True,
            max_reasoning_iterations=1,
            modalities=["string"],
            model="model",
            persona_id="persona_id",
            project_id="project_id",
            session_id="session_id",
            skip_initial_retrieval=True,
            stream=True,
            use_reasoning=True,
            video_refs={"foo": "string"},
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create_completion(self, client: ElicitClient) -> None:
        response = client.chat.with_raw_response.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = response.parse()
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create_completion(self, client: ElicitClient) -> None:
        with client.chat.with_streaming_response.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = response.parse()
            assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncChat:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_completion(self, async_client: AsyncElicitClient) -> None:
        chat = await async_client.chat.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_completion_with_all_params(self, async_client: AsyncElicitClient) -> None:
        chat = await async_client.chat.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
            agent_mode=True,
            audio_config={
                "audio_type": "audio_type",
                "duration": 0,
                "model": "model",
                "speed": 0.25,
                "voice": "voice",
            },
            auto_detect_agent=True,
            disabled_learning=True,
            history_limit=1,
            image_config={
                "model": "model",
                "seed": 0,
                "size": "size",
            },
            load_history=True,
            max_reasoning_iterations=1,
            modalities=["string"],
            model="model",
            persona_id="persona_id",
            project_id="project_id",
            session_id="session_id",
            skip_initial_retrieval=True,
            stream=True,
            use_reasoning=True,
            video_refs={"foo": "string"},
        )
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create_completion(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.chat.with_raw_response.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        chat = await response.parse()
        assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create_completion(self, async_client: AsyncElicitClient) -> None:
        async with async_client.chat.with_streaming_response.create_completion(
            messages=[
                {
                    "content": "string",
                    "role": "role",
                }
            ],
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            chat = await response.parse()
            assert_matches_type(ChatCreateCompletionResponse, chat, path=["response"])

        assert cast(Any, response.is_closed) is True
