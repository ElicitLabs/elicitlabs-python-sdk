# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import ModalLearnResponse, ModalQueryResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModal:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_learn(self, client: ElicitClient) -> None:
        modal = client.modal.learn(
            messages=[
                {"content": "job_id_123"},
                {"content": "The animation is too slow"},
                {"content": "Good catch. Let's remember to speed it up to 200ms for the next sprint."},
            ],
            user_id="user_123",
        )
        assert_matches_type(ModalLearnResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_learn_with_all_params(self, client: ElicitClient) -> None:
        modal = client.modal.learn(
            messages=[
                {
                    "content": "job_id_123",
                    "role": "role",
                    "type": "image",
                },
                {
                    "content": "The animation is too slow",
                    "role": "role",
                    "type": "feedback",
                },
                {
                    "content": "Good catch. Let's remember to speed it up to 200ms for the next sprint.",
                    "role": "user",
                    "type": "type",
                },
            ],
            user_id="user_123",
            persona_id="persona_id",
            project_id="proj_ABC",
            session_id="session_123",
            timestamp="2026-02-07T12:00:00Z",
        )
        assert_matches_type(ModalLearnResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_learn(self, client: ElicitClient) -> None:
        response = client.modal.with_raw_response.learn(
            messages=[
                {"content": "job_id_123"},
                {"content": "The animation is too slow"},
                {"content": "Good catch. Let's remember to speed it up to 200ms for the next sprint."},
            ],
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalLearnResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_learn(self, client: ElicitClient) -> None:
        with client.modal.with_streaming_response.learn(
            messages=[
                {"content": "job_id_123"},
                {"content": "The animation is too slow"},
                {"content": "Good catch. Let's remember to speed it up to 200ms for the next sprint."},
            ],
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalLearnResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_query(self, client: ElicitClient) -> None:
        modal = client.modal.query(
            user_id="user_123",
        )
        assert_matches_type(ModalQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_query_with_all_params(self, client: ElicitClient) -> None:
        modal = client.modal.query(
            user_id="user_123",
            audio_base64="audio_base64",
            image_base64="image_base64",
            include_modalities=["text", "video"],
            persona_id="persona_id",
            project_id="proj_ABC",
            session_id="session_id",
            text_input="text_input",
            video_base64="video_base64",
        )
        assert_matches_type(ModalQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_query(self, client: ElicitClient) -> None:
        response = client.modal.with_raw_response.query(
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_query(self, client: ElicitClient) -> None:
        with client.modal.with_streaming_response.query(
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalQueryResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncModal:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_learn(self, async_client: AsyncElicitClient) -> None:
        modal = await async_client.modal.learn(
            messages=[
                {"content": "job_id_123"},
                {"content": "The animation is too slow"},
                {"content": "Good catch. Let's remember to speed it up to 200ms for the next sprint."},
            ],
            user_id="user_123",
        )
        assert_matches_type(ModalLearnResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_learn_with_all_params(self, async_client: AsyncElicitClient) -> None:
        modal = await async_client.modal.learn(
            messages=[
                {
                    "content": "job_id_123",
                    "role": "role",
                    "type": "image",
                },
                {
                    "content": "The animation is too slow",
                    "role": "role",
                    "type": "feedback",
                },
                {
                    "content": "Good catch. Let's remember to speed it up to 200ms for the next sprint.",
                    "role": "user",
                    "type": "type",
                },
            ],
            user_id="user_123",
            persona_id="persona_id",
            project_id="proj_ABC",
            session_id="session_123",
            timestamp="2026-02-07T12:00:00Z",
        )
        assert_matches_type(ModalLearnResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_learn(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.modal.with_raw_response.learn(
            messages=[
                {"content": "job_id_123"},
                {"content": "The animation is too slow"},
                {"content": "Good catch. Let's remember to speed it up to 200ms for the next sprint."},
            ],
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalLearnResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_learn(self, async_client: AsyncElicitClient) -> None:
        async with async_client.modal.with_streaming_response.learn(
            messages=[
                {"content": "job_id_123"},
                {"content": "The animation is too slow"},
                {"content": "Good catch. Let's remember to speed it up to 200ms for the next sprint."},
            ],
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalLearnResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_query(self, async_client: AsyncElicitClient) -> None:
        modal = await async_client.modal.query(
            user_id="user_123",
        )
        assert_matches_type(ModalQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncElicitClient) -> None:
        modal = await async_client.modal.query(
            user_id="user_123",
            audio_base64="audio_base64",
            image_base64="image_base64",
            include_modalities=["text", "video"],
            persona_id="persona_id",
            project_id="proj_ABC",
            session_id="session_id",
            text_input="text_input",
            video_base64="video_base64",
        )
        assert_matches_type(ModalQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_query(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.modal.with_raw_response.query(
            user_id="user_123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncElicitClient) -> None:
        async with async_client.modal.with_streaming_response.query(
            user_id="user_123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalQueryResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True
