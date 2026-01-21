# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import (
    InferenceGenerateCompletionResponse,
    InferenceGeneratePersonaChatResponse,
    InferenceGenerateMultimodalityCompletionResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInference:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_completion(self, client: ElicitClient) -> None:
        inference = client.inference.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
        )
        assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_completion_with_all_params(self, client: ElicitClient) -> None:
        inference = client.inference.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
            disabled_learning=False,
            model="gpt-4.1-mini",
            persona_id="persona_id",
            project_id="project_id",
            session_id="session-abc",
        )
        assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate_completion(self, client: ElicitClient) -> None:
        response = client.inference.with_raw_response.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = response.parse()
        assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate_completion(self, client: ElicitClient) -> None:
        with client.inference.with_streaming_response.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = response.parse()
            assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_multimodality_completion(self, client: ElicitClient) -> None:
        inference = client.inference.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_multimodality_completion_with_all_params(self, client: ElicitClient) -> None:
        inference = client.inference.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
            audio_base64="base64_encoded_audio...",
            context="context",
            disabled_learning=False,
            image_base64="base64_encoded_image...",
            model="gemini-2.5-flash",
            output_type="text",
            persona_id="persona_id",
            project_id="project_id",
            question="What do you see?",
            session_id="session_123",
            speed=1,
            video_base64="base64_encoded_video...",
            voice="alloy",
        )
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate_multimodality_completion(self, client: ElicitClient) -> None:
        response = client.inference.with_raw_response.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = response.parse()
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate_multimodality_completion(self, client: ElicitClient) -> None:
        with client.inference.with_streaming_response.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = response.parse()
            assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_persona_chat(self, client: ElicitClient) -> None:
        inference = client.inference.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
        )
        assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_persona_chat_with_all_params(self, client: ElicitClient) -> None:
        inference = client.inference.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
            disabled_learning=True,
            model="gpt-4.1-mini",
            session_id="session-abc",
        )
        assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate_persona_chat(self, client: ElicitClient) -> None:
        response = client.inference.with_raw_response.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = response.parse()
        assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate_persona_chat(self, client: ElicitClient) -> None:
        with client.inference.with_streaming_response.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = response.parse()
            assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInference:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_completion(self, async_client: AsyncElicitClient) -> None:
        inference = await async_client.inference.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
        )
        assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_completion_with_all_params(self, async_client: AsyncElicitClient) -> None:
        inference = await async_client.inference.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
            disabled_learning=False,
            model="gpt-4.1-mini",
            persona_id="persona_id",
            project_id="project_id",
            session_id="session-abc",
        )
        assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate_completion(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.inference.with_raw_response.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = await response.parse()
        assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate_completion(self, async_client: AsyncElicitClient) -> None:
        async with async_client.inference.with_streaming_response.generate_completion(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            user_id="user-123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = await response.parse()
            assert_matches_type(InferenceGenerateCompletionResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_multimodality_completion(self, async_client: AsyncElicitClient) -> None:
        inference = await async_client.inference.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_multimodality_completion_with_all_params(
        self, async_client: AsyncElicitClient
    ) -> None:
        inference = await async_client.inference.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
            audio_base64="base64_encoded_audio...",
            context="context",
            disabled_learning=False,
            image_base64="base64_encoded_image...",
            model="gemini-2.5-flash",
            output_type="text",
            persona_id="persona_id",
            project_id="project_id",
            question="What do you see?",
            session_id="session_123",
            speed=1,
            video_base64="base64_encoded_video...",
            voice="alloy",
        )
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate_multimodality_completion(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.inference.with_raw_response.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = await response.parse()
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate_multimodality_completion(self, async_client: AsyncElicitClient) -> None:
        async with async_client.inference.with_streaming_response.generate_multimodality_completion(
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = await response.parse()
            assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_persona_chat(self, async_client: AsyncElicitClient) -> None:
        inference = await async_client.inference.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
        )
        assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_persona_chat_with_all_params(self, async_client: AsyncElicitClient) -> None:
        inference = await async_client.inference.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
            disabled_learning=True,
            model="gpt-4.1-mini",
            session_id="session-abc",
        )
        assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate_persona_chat(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.inference.with_raw_response.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = await response.parse()
        assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate_persona_chat(self, async_client: AsyncElicitClient) -> None:
        async with async_client.inference.with_streaming_response.generate_persona_chat(
            content=[
                {
                    "content": "You are a helpful AI assistant.",
                    "role": "system",
                },
                {
                    "content": "Hello, how are you?",
                    "role": "user",
                },
            ],
            persona_id="persona-456",
            user_id="user-123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            inference = await response.parse()
            assert_matches_type(InferenceGeneratePersonaChatResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True
