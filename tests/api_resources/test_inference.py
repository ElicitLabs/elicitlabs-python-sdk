# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import (
    InferenceGenerateCompletionResponse,
    InferenceGenerateMultimodalityCompletionResponse,
)

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestInference:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_completion(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_completion_with_all_params(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_generate_completion(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_generate_completion(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_multimodality_completion(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            inference = client.inference.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
            )

        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_generate_multimodality_completion_with_all_params(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            inference = client.inference.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
                audio_base64="base64_encoded_audio...",
                audio_duration=0,
                audio_type="tts",
                context="context",
                disabled_learning=False,
                image_base64="base64_encoded_image...",
                max_reasoning_iterations=1,
                model="gemini-2.5-flash",
                num_images=1,
                output_type="text",
                persona_id="persona_id",
                project_id="project_id",
                question="What do you see?",
                seed=0,
                session_id="session_123",
                speed=1,
                use_reasoning=True,
                video_base64="base64_encoded_video...",
                voice="alloy",
            )

        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_generate_multimodality_completion(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.inference.with_raw_response.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = response.parse()
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_generate_multimodality_completion(self, client: ElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            with client.inference.with_streaming_response.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                inference = response.parse()
                assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncInference:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_completion(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_completion_with_all_params(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_generate_completion(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_generate_completion(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
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

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_multimodality_completion(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            inference = await async_client.inference.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
            )

        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_generate_multimodality_completion_with_all_params(
        self, async_client: AsyncElicitClient
    ) -> None:
        with pytest.warns(DeprecationWarning):
            inference = await async_client.inference.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
                audio_base64="base64_encoded_audio...",
                audio_duration=0,
                audio_type="tts",
                context="context",
                disabled_learning=False,
                image_base64="base64_encoded_image...",
                max_reasoning_iterations=1,
                model="gemini-2.5-flash",
                num_images=1,
                output_type="text",
                persona_id="persona_id",
                project_id="project_id",
                question="What do you see?",
                seed=0,
                session_id="session_123",
                speed=1,
                use_reasoning=True,
                video_base64="base64_encoded_video...",
                voice="alloy",
            )

        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_generate_multimodality_completion(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.inference.with_raw_response.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        inference = await response.parse()
        assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_generate_multimodality_completion(self, async_client: AsyncElicitClient) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.inference.with_streaming_response.generate_multimodality_completion(
                user_id="123e4567-e89b-12d3-a456-426614174000",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                inference = await response.parse()
                assert_matches_type(InferenceGenerateMultimodalityCompletionResponse, inference, path=["response"])

        assert cast(Any, response.is_closed) is True
