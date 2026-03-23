# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from tests.utils import assert_matches_type
from elicitlabs.types.personas import LinkCreateResponse, LinkDeleteResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLink:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: ElicitClient) -> None:
        link = client.personas.link.create(
            persona_id="persona_id",
            user_id="user_id",
        )
        assert_matches_type(LinkCreateResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: ElicitClient) -> None:
        response = client.personas.link.with_raw_response.create(
            persona_id="persona_id",
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        link = response.parse()
        assert_matches_type(LinkCreateResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: ElicitClient) -> None:
        with client.personas.link.with_streaming_response.create(
            persona_id="persona_id",
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            link = response.parse()
            assert_matches_type(LinkCreateResponse, link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_create(self, client: ElicitClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `persona_id` but received ''"):
            client.personas.link.with_raw_response.create(
                persona_id="",
                user_id="user_id",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_delete(self, client: ElicitClient) -> None:
        link = client.personas.link.delete(
            user_id="user_id",
            persona_id="persona_id",
        )
        assert_matches_type(LinkDeleteResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_delete(self, client: ElicitClient) -> None:
        response = client.personas.link.with_raw_response.delete(
            user_id="user_id",
            persona_id="persona_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        link = response.parse()
        assert_matches_type(LinkDeleteResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_delete(self, client: ElicitClient) -> None:
        with client.personas.link.with_streaming_response.delete(
            user_id="user_id",
            persona_id="persona_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            link = response.parse()
            assert_matches_type(LinkDeleteResponse, link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_path_params_delete(self, client: ElicitClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `persona_id` but received ''"):
            client.personas.link.with_raw_response.delete(
                user_id="user_id",
                persona_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            client.personas.link.with_raw_response.delete(
                user_id="",
                persona_id="persona_id",
            )


class TestAsyncLink:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncElicitClient) -> None:
        link = await async_client.personas.link.create(
            persona_id="persona_id",
            user_id="user_id",
        )
        assert_matches_type(LinkCreateResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.personas.link.with_raw_response.create(
            persona_id="persona_id",
            user_id="user_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        link = await response.parse()
        assert_matches_type(LinkCreateResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncElicitClient) -> None:
        async with async_client.personas.link.with_streaming_response.create(
            persona_id="persona_id",
            user_id="user_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            link = await response.parse()
            assert_matches_type(LinkCreateResponse, link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_create(self, async_client: AsyncElicitClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `persona_id` but received ''"):
            await async_client.personas.link.with_raw_response.create(
                persona_id="",
                user_id="user_id",
            )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_delete(self, async_client: AsyncElicitClient) -> None:
        link = await async_client.personas.link.delete(
            user_id="user_id",
            persona_id="persona_id",
        )
        assert_matches_type(LinkDeleteResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncElicitClient) -> None:
        response = await async_client.personas.link.with_raw_response.delete(
            user_id="user_id",
            persona_id="persona_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        link = await response.parse()
        assert_matches_type(LinkDeleteResponse, link, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncElicitClient) -> None:
        async with async_client.personas.link.with_streaming_response.delete(
            user_id="user_id",
            persona_id="persona_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            link = await response.parse()
            assert_matches_type(LinkDeleteResponse, link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncElicitClient) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `persona_id` but received ''"):
            await async_client.personas.link.with_raw_response.delete(
                user_id="user_id",
                persona_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `user_id` but received ''"):
            await async_client.personas.link.with_raw_response.delete(
                user_id="",
                persona_id="persona_id",
            )
