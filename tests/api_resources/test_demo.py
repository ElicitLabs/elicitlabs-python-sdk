# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types import (
    DemoSignInResponse,
    DemoCreateUserResponse,
    DemoResetPasswordResponse,
    DemoGenerateResetLinkResponse,
    DemoRetrieveCurrentUserResponse,
    DemoRequestPasswordResetResponse,
    DemoSubmitEarlyAccessRequestResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestDemo:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_user(self, client: ElicitClient) -> None:
        demo = client.demo.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
        )
        assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_create_user_with_all_params(self, client: ElicitClient) -> None:
        demo = client.demo.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
            org_id="org_id",
        )
        assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_create_user(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_create_user(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_generate_reset_link(self, client: ElicitClient) -> None:
        demo = client.demo.generate_reset_link(
            email="user@example.com",
        )
        assert_matches_type(DemoGenerateResetLinkResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_generate_reset_link(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.generate_reset_link(
            email="user@example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoGenerateResetLinkResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_generate_reset_link(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.generate_reset_link(
            email="user@example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoGenerateResetLinkResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_request_password_reset(self, client: ElicitClient) -> None:
        demo = client.demo.request_password_reset(
            email="user@example.com",
        )
        assert_matches_type(DemoRequestPasswordResetResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_request_password_reset(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.request_password_reset(
            email="user@example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoRequestPasswordResetResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_request_password_reset(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.request_password_reset(
            email="user@example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoRequestPasswordResetResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_reset_password(self, client: ElicitClient) -> None:
        demo = client.demo.reset_password(
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            confirm_password="newpassword456",
            new_password="newpassword456",
        )
        assert_matches_type(DemoResetPasswordResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_reset_password(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.reset_password(
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            confirm_password="newpassword456",
            new_password="newpassword456",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoResetPasswordResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_reset_password(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.reset_password(
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            confirm_password="newpassword456",
            new_password="newpassword456",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoResetPasswordResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_retrieve_current_user(self, client: ElicitClient) -> None:
        demo = client.demo.retrieve_current_user()
        assert_matches_type(DemoRetrieveCurrentUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_retrieve_current_user(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.retrieve_current_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoRetrieveCurrentUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_retrieve_current_user(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.retrieve_current_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoRetrieveCurrentUserResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_sign_in(self, client: ElicitClient) -> None:
        demo = client.demo.sign_in(
            email="user@example.com",
            password="securepassword123",
        )
        assert_matches_type(DemoSignInResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_sign_in(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.sign_in(
            email="user@example.com",
            password="securepassword123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoSignInResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_sign_in(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.sign_in(
            email="user@example.com",
            password="securepassword123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoSignInResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_submit_early_access_request(self, client: ElicitClient) -> None:
        demo = client.demo.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
        )
        assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_method_submit_early_access_request_with_all_params(self, client: ElicitClient) -> None:
        demo = client.demo.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
            company_size="company_size",
            industry="SaaS",
            role="CTO",
        )
        assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_raw_response_submit_early_access_request(self, client: ElicitClient) -> None:
        response = client.demo.with_raw_response.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = response.parse()
        assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    def test_streaming_response_submit_early_access_request(self, client: ElicitClient) -> None:
        with client.demo.with_streaming_response.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = response.parse()
            assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncDemo:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_user(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
        )
        assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_create_user_with_all_params(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
            org_id="org_id",
        )
        assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_create_user(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_create_user(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.create_user(
            email="user@example.com",
            name="John Doe",
            password="securepassword123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoCreateUserResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_generate_reset_link(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.generate_reset_link(
            email="user@example.com",
        )
        assert_matches_type(DemoGenerateResetLinkResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_generate_reset_link(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.generate_reset_link(
            email="user@example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoGenerateResetLinkResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_generate_reset_link(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.generate_reset_link(
            email="user@example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoGenerateResetLinkResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_request_password_reset(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.request_password_reset(
            email="user@example.com",
        )
        assert_matches_type(DemoRequestPasswordResetResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_request_password_reset(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.request_password_reset(
            email="user@example.com",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoRequestPasswordResetResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_request_password_reset(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.request_password_reset(
            email="user@example.com",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoRequestPasswordResetResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_reset_password(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.reset_password(
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            confirm_password="newpassword456",
            new_password="newpassword456",
        )
        assert_matches_type(DemoResetPasswordResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_reset_password(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.reset_password(
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            confirm_password="newpassword456",
            new_password="newpassword456",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoResetPasswordResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_reset_password(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.reset_password(
            token="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            confirm_password="newpassword456",
            new_password="newpassword456",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoResetPasswordResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_retrieve_current_user(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.retrieve_current_user()
        assert_matches_type(DemoRetrieveCurrentUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_retrieve_current_user(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.retrieve_current_user()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoRetrieveCurrentUserResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_retrieve_current_user(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.retrieve_current_user() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoRetrieveCurrentUserResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_sign_in(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.sign_in(
            email="user@example.com",
            password="securepassword123",
        )
        assert_matches_type(DemoSignInResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_sign_in(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.sign_in(
            email="user@example.com",
            password="securepassword123",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoSignInResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_sign_in(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.sign_in(
            email="user@example.com",
            password="securepassword123",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoSignInResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_submit_early_access_request(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
        )
        assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_method_submit_early_access_request_with_all_params(self, async_client: AsyncElicitClient) -> None:
        demo = await async_client.demo.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
            company_size="company_size",
            industry="SaaS",
            role="CTO",
        )
        assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_raw_response_submit_early_access_request(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.demo.with_raw_response.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        demo = await response.parse()
        assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

    @pytest.mark.skip(reason="Prism tests are disabled")
    @parametrize
    async def test_streaming_response_submit_early_access_request(self, async_client: AsyncElicitClient) -> None:
        async with async_client.demo.with_streaming_response.submit_early_access_request(
            email="user@example.com",
            name="John Doe",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            demo = await response.parse()
            assert_matches_type(DemoSubmitEarlyAccessRequestResponse, demo, path=["response"])

        assert cast(Any, response.is_closed) is True
