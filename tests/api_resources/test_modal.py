# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicit_labs import ElicitLabs, AsyncElicitLabs
from tests.utils import assert_matches_type
from elicit_labs.types import (
    ModalInitializeResponse,
    ModalAnalyzeTextResponse,
    ModalRespondToQueryResponse,
    ModalAnswerBackslashQueryResponse,
    ModalGenerateAutocompleteResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestModal:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_analyze_text(self, client: ElicitLabs) -> None:
        modal = client.modal.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_analyze_text_with_all_params(self, client: ElicitLabs) -> None:
        modal = client.modal.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            conversation_history=[
                {
                    "content": "bar",
                    "role": "bar",
                },
                {
                    "content": "bar",
                    "role": "bar",
                },
            ],
            document_type="email",
            session_id="reflection_session_123",
        )
        assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_analyze_text(self, client: ElicitLabs) -> None:
        response = client.modal.with_raw_response.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_analyze_text(self, client: ElicitLabs) -> None:
        with client.modal.with_streaming_response.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_answer_backslash_query(self, client: ElicitLabs) -> None:
        modal = client.modal.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_answer_backslash_query_with_all_params(self, client: ElicitLabs) -> None:
        modal = client.modal.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            conversation_history=[
                {
                    "content": "bar",
                    "role": "bar",
                },
                {
                    "content": "bar",
                    "role": "bar",
                },
            ],
            document_type="email",
            session_id="backslash_q_session_123",
        )
        assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_answer_backslash_query(self, client: ElicitLabs) -> None:
        response = client.modal.with_raw_response.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_answer_backslash_query(self, client: ElicitLabs) -> None:
        with client.modal.with_streaming_response.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_autocomplete(self, client: ElicitLabs) -> None:
        modal = client.modal.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_autocomplete_with_all_params(self, client: ElicitLabs) -> None:
        modal = client.modal.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            conversation_history=[
                {
                    "content": "bar",
                    "role": "bar",
                },
                {
                    "content": "bar",
                    "role": "bar",
                },
            ],
            document_type="email",
            session_id="demo_session_123",
        )
        assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate_autocomplete(self, client: ElicitLabs) -> None:
        response = client.modal.with_raw_response.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate_autocomplete(self, client: ElicitLabs) -> None:
        with client.modal.with_streaming_response.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_initialize(self, client: ElicitLabs) -> None:
        modal = client.modal.initialize(
            app_context={"app_name": "Mail"},
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalInitializeResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_initialize_with_all_params(self, client: ElicitLabs) -> None:
        modal = client.modal.initialize(
            app_context={
                "app_name": "Mail",
                "app_type": "email_client",
                "app_version": "2024.1",
            },
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            screenshot_base64="screenshot_base64",
            screenshot_path="path/to/email_screenshot.png",
        )
        assert_matches_type(ModalInitializeResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_initialize(self, client: ElicitLabs) -> None:
        response = client.modal.with_raw_response.initialize(
            app_context={"app_name": "Mail"},
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalInitializeResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_initialize(self, client: ElicitLabs) -> None:
        with client.modal.with_streaming_response.initialize(
            app_context={"app_name": "Mail"},
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalInitializeResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_respond_to_query(self, client: ElicitLabs) -> None:
        modal = client.modal.respond_to_query(
            message="Hello, how are you?",
            session_id="demo_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalRespondToQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_respond_to_query(self, client: ElicitLabs) -> None:
        response = client.modal.with_raw_response.respond_to_query(
            message="Hello, how are you?",
            session_id="demo_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = response.parse()
        assert_matches_type(ModalRespondToQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_respond_to_query(self, client: ElicitLabs) -> None:
        with client.modal.with_streaming_response.respond_to_query(
            message="Hello, how are you?",
            session_id="demo_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = response.parse()
            assert_matches_type(ModalRespondToQueryResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncModal:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_analyze_text(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_analyze_text_with_all_params(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            conversation_history=[
                {
                    "content": "bar",
                    "role": "bar",
                },
                {
                    "content": "bar",
                    "role": "bar",
                },
            ],
            document_type="email",
            session_id="reflection_session_123",
        )
        assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_analyze_text(self, async_client: AsyncElicitLabs) -> None:
        response = await async_client.modal.with_raw_response.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_analyze_text(self, async_client: AsyncElicitLabs) -> None:
        async with async_client.modal.with_streaming_response.analyze_text(
            text_to_analyze="Hello, I hope this email finds you well. I wanted to follow up on our meeting yesteday about the quaterly budget.",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalAnalyzeTextResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_answer_backslash_query(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_answer_backslash_query_with_all_params(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            conversation_history=[
                {
                    "content": "bar",
                    "role": "bar",
                },
                {
                    "content": "bar",
                    "role": "bar",
                },
            ],
            document_type="email",
            session_id="backslash_q_session_123",
        )
        assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_answer_backslash_query(self, async_client: AsyncElicitLabs) -> None:
        response = await async_client.modal.with_raw_response.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_answer_backslash_query(self, async_client: AsyncElicitLabs) -> None:
        async with async_client.modal.with_streaming_response.answer_backslash_query(
            context_text="I'll be available for the meeting on [QUERY]. Let me know what works best for you.",
            query="when am I free next week?",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalAnswerBackslashQueryResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_autocomplete(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_autocomplete_with_all_params(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            conversation_history=[
                {
                    "content": "bar",
                    "role": "bar",
                },
                {
                    "content": "bar",
                    "role": "bar",
                },
            ],
            document_type="email",
            session_id="demo_session_123",
        )
        assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate_autocomplete(self, async_client: AsyncElicitLabs) -> None:
        response = await async_client.modal.with_raw_response.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate_autocomplete(self, async_client: AsyncElicitLabs) -> None:
        async with async_client.modal.with_streaming_response.generate_autocomplete(
            partial_text="I'm thinking about visiting",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalGenerateAutocompleteResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_initialize(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.initialize(
            app_context={"app_name": "Mail"},
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalInitializeResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_initialize_with_all_params(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.initialize(
            app_context={
                "app_name": "Mail",
                "app_type": "email_client",
                "app_version": "2024.1",
            },
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
            screenshot_base64="screenshot_base64",
            screenshot_path="path/to/email_screenshot.png",
        )
        assert_matches_type(ModalInitializeResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_initialize(self, async_client: AsyncElicitLabs) -> None:
        response = await async_client.modal.with_raw_response.initialize(
            app_context={"app_name": "Mail"},
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalInitializeResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_initialize(self, async_client: AsyncElicitLabs) -> None:
        async with async_client.modal.with_streaming_response.initialize(
            app_context={"app_name": "Mail"},
            session_id="modal_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalInitializeResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_respond_to_query(self, async_client: AsyncElicitLabs) -> None:
        modal = await async_client.modal.respond_to_query(
            message="Hello, how are you?",
            session_id="demo_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )
        assert_matches_type(ModalRespondToQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_respond_to_query(self, async_client: AsyncElicitLabs) -> None:
        response = await async_client.modal.with_raw_response.respond_to_query(
            message="Hello, how are you?",
            session_id="demo_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        modal = await response.parse()
        assert_matches_type(ModalRespondToQueryResponse, modal, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_respond_to_query(self, async_client: AsyncElicitLabs) -> None:
        async with async_client.modal.with_streaming_response.respond_to_query(
            message="Hello, how are you?",
            session_id="demo_session_123",
            user_id="123e4567-e89b-12d3-a456-426614174000",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            modal = await response.parse()
            assert_matches_type(ModalRespondToQueryResponse, modal, path=["response"])

        assert cast(Any, response.is_closed) is True
