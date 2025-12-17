# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import APIStatusError, ElicitClientError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import auth, data, demo, modal, users, health, personas, inference
    from .resources.modal import ModalResource, AsyncModalResource
    from .resources.users import UsersResource, AsyncUsersResource
    from .resources.health import HealthResource, AsyncHealthResource
    from .resources.personas import PersonasResource, AsyncPersonasResource
    from .resources.auth.auth import AuthResource, AsyncAuthResource
    from .resources.data.data import DataResource, AsyncDataResource
    from .resources.demo.demo import DemoResource, AsyncDemoResource
    from .resources.inference import InferenceResource, AsyncInferenceResource

__all__ = [
    "Timeout",
    "Transport",
    "ProxiesTypes",
    "RequestOptions",
    "ElicitClient",
    "AsyncElicitClient",
    "Client",
    "AsyncClient",
]


class ElicitClient(SyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous ElicitClient client instance.

        This automatically infers the `api_key` argument from the `ELICIT_LABS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("ELICIT_LABS_API_KEY")
        if api_key is None:
            raise ElicitClientError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ELICIT_LABS_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ELICIT_CLIENT_BASE_URL")
        if base_url is None:
            base_url = f"https://api.elicitlabs.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def modal(self) -> ModalResource:
        from .resources.modal import ModalResource

        return ModalResource(self)

    @cached_property
    def users(self) -> UsersResource:
        from .resources.users import UsersResource

        return UsersResource(self)

    @cached_property
    def data(self) -> DataResource:
        from .resources.data import DataResource

        return DataResource(self)

    @cached_property
    def health(self) -> HealthResource:
        from .resources.health import HealthResource

        return HealthResource(self)

    @cached_property
    def auth(self) -> AuthResource:
        from .resources.auth import AuthResource

        return AuthResource(self)

    @cached_property
    def personas(self) -> PersonasResource:
        from .resources.personas import PersonasResource

        return PersonasResource(self)

    @cached_property
    def inference(self) -> InferenceResource:
        from .resources.inference import InferenceResource

        return InferenceResource(self)

    @cached_property
    def demo(self) -> DemoResource:
        from .resources.demo import DemoResource

        return DemoResource(self)

    @cached_property
    def with_raw_response(self) -> ElicitClientWithRawResponse:
        return ElicitClientWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ElicitClientWithStreamedResponse:
        return ElicitClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncElicitClient(AsyncAPIClient):
    # client options
    api_key: str

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncElicitClient client instance.

        This automatically infers the `api_key` argument from the `ELICIT_LABS_API_KEY` environment variable if it is not provided.
        """
        if api_key is None:
            api_key = os.environ.get("ELICIT_LABS_API_KEY")
        if api_key is None:
            raise ElicitClientError(
                "The api_key client option must be set either by passing api_key to the client or by setting the ELICIT_LABS_API_KEY environment variable"
            )
        self.api_key = api_key

        if base_url is None:
            base_url = os.environ.get("ELICIT_CLIENT_BASE_URL")
        if base_url is None:
            base_url = f"https://api.elicitlabs.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

    @cached_property
    def modal(self) -> AsyncModalResource:
        from .resources.modal import AsyncModalResource

        return AsyncModalResource(self)

    @cached_property
    def users(self) -> AsyncUsersResource:
        from .resources.users import AsyncUsersResource

        return AsyncUsersResource(self)

    @cached_property
    def data(self) -> AsyncDataResource:
        from .resources.data import AsyncDataResource

        return AsyncDataResource(self)

    @cached_property
    def health(self) -> AsyncHealthResource:
        from .resources.health import AsyncHealthResource

        return AsyncHealthResource(self)

    @cached_property
    def auth(self) -> AsyncAuthResource:
        from .resources.auth import AsyncAuthResource

        return AsyncAuthResource(self)

    @cached_property
    def personas(self) -> AsyncPersonasResource:
        from .resources.personas import AsyncPersonasResource

        return AsyncPersonasResource(self)

    @cached_property
    def inference(self) -> AsyncInferenceResource:
        from .resources.inference import AsyncInferenceResource

        return AsyncInferenceResource(self)

    @cached_property
    def demo(self) -> AsyncDemoResource:
        from .resources.demo import AsyncDemoResource

        return AsyncDemoResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncElicitClientWithRawResponse:
        return AsyncElicitClientWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncElicitClientWithStreamedResponse:
        return AsyncElicitClientWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        api_key = self.api_key
        return {"Authorization": f"Bearer {api_key}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        api_key: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            api_key=api_key or self.api_key,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class ElicitClientWithRawResponse:
    _client: ElicitClient

    def __init__(self, client: ElicitClient) -> None:
        self._client = client

    @cached_property
    def modal(self) -> modal.ModalResourceWithRawResponse:
        from .resources.modal import ModalResourceWithRawResponse

        return ModalResourceWithRawResponse(self._client.modal)

    @cached_property
    def users(self) -> users.UsersResourceWithRawResponse:
        from .resources.users import UsersResourceWithRawResponse

        return UsersResourceWithRawResponse(self._client.users)

    @cached_property
    def data(self) -> data.DataResourceWithRawResponse:
        from .resources.data import DataResourceWithRawResponse

        return DataResourceWithRawResponse(self._client.data)

    @cached_property
    def health(self) -> health.HealthResourceWithRawResponse:
        from .resources.health import HealthResourceWithRawResponse

        return HealthResourceWithRawResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AuthResourceWithRawResponse:
        from .resources.auth import AuthResourceWithRawResponse

        return AuthResourceWithRawResponse(self._client.auth)

    @cached_property
    def personas(self) -> personas.PersonasResourceWithRawResponse:
        from .resources.personas import PersonasResourceWithRawResponse

        return PersonasResourceWithRawResponse(self._client.personas)

    @cached_property
    def inference(self) -> inference.InferenceResourceWithRawResponse:
        from .resources.inference import InferenceResourceWithRawResponse

        return InferenceResourceWithRawResponse(self._client.inference)

    @cached_property
    def demo(self) -> demo.DemoResourceWithRawResponse:
        from .resources.demo import DemoResourceWithRawResponse

        return DemoResourceWithRawResponse(self._client.demo)


class AsyncElicitClientWithRawResponse:
    _client: AsyncElicitClient

    def __init__(self, client: AsyncElicitClient) -> None:
        self._client = client

    @cached_property
    def modal(self) -> modal.AsyncModalResourceWithRawResponse:
        from .resources.modal import AsyncModalResourceWithRawResponse

        return AsyncModalResourceWithRawResponse(self._client.modal)

    @cached_property
    def users(self) -> users.AsyncUsersResourceWithRawResponse:
        from .resources.users import AsyncUsersResourceWithRawResponse

        return AsyncUsersResourceWithRawResponse(self._client.users)

    @cached_property
    def data(self) -> data.AsyncDataResourceWithRawResponse:
        from .resources.data import AsyncDataResourceWithRawResponse

        return AsyncDataResourceWithRawResponse(self._client.data)

    @cached_property
    def health(self) -> health.AsyncHealthResourceWithRawResponse:
        from .resources.health import AsyncHealthResourceWithRawResponse

        return AsyncHealthResourceWithRawResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AsyncAuthResourceWithRawResponse:
        from .resources.auth import AsyncAuthResourceWithRawResponse

        return AsyncAuthResourceWithRawResponse(self._client.auth)

    @cached_property
    def personas(self) -> personas.AsyncPersonasResourceWithRawResponse:
        from .resources.personas import AsyncPersonasResourceWithRawResponse

        return AsyncPersonasResourceWithRawResponse(self._client.personas)

    @cached_property
    def inference(self) -> inference.AsyncInferenceResourceWithRawResponse:
        from .resources.inference import AsyncInferenceResourceWithRawResponse

        return AsyncInferenceResourceWithRawResponse(self._client.inference)

    @cached_property
    def demo(self) -> demo.AsyncDemoResourceWithRawResponse:
        from .resources.demo import AsyncDemoResourceWithRawResponse

        return AsyncDemoResourceWithRawResponse(self._client.demo)


class ElicitClientWithStreamedResponse:
    _client: ElicitClient

    def __init__(self, client: ElicitClient) -> None:
        self._client = client

    @cached_property
    def modal(self) -> modal.ModalResourceWithStreamingResponse:
        from .resources.modal import ModalResourceWithStreamingResponse

        return ModalResourceWithStreamingResponse(self._client.modal)

    @cached_property
    def users(self) -> users.UsersResourceWithStreamingResponse:
        from .resources.users import UsersResourceWithStreamingResponse

        return UsersResourceWithStreamingResponse(self._client.users)

    @cached_property
    def data(self) -> data.DataResourceWithStreamingResponse:
        from .resources.data import DataResourceWithStreamingResponse

        return DataResourceWithStreamingResponse(self._client.data)

    @cached_property
    def health(self) -> health.HealthResourceWithStreamingResponse:
        from .resources.health import HealthResourceWithStreamingResponse

        return HealthResourceWithStreamingResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AuthResourceWithStreamingResponse:
        from .resources.auth import AuthResourceWithStreamingResponse

        return AuthResourceWithStreamingResponse(self._client.auth)

    @cached_property
    def personas(self) -> personas.PersonasResourceWithStreamingResponse:
        from .resources.personas import PersonasResourceWithStreamingResponse

        return PersonasResourceWithStreamingResponse(self._client.personas)

    @cached_property
    def inference(self) -> inference.InferenceResourceWithStreamingResponse:
        from .resources.inference import InferenceResourceWithStreamingResponse

        return InferenceResourceWithStreamingResponse(self._client.inference)

    @cached_property
    def demo(self) -> demo.DemoResourceWithStreamingResponse:
        from .resources.demo import DemoResourceWithStreamingResponse

        return DemoResourceWithStreamingResponse(self._client.demo)


class AsyncElicitClientWithStreamedResponse:
    _client: AsyncElicitClient

    def __init__(self, client: AsyncElicitClient) -> None:
        self._client = client

    @cached_property
    def modal(self) -> modal.AsyncModalResourceWithStreamingResponse:
        from .resources.modal import AsyncModalResourceWithStreamingResponse

        return AsyncModalResourceWithStreamingResponse(self._client.modal)

    @cached_property
    def users(self) -> users.AsyncUsersResourceWithStreamingResponse:
        from .resources.users import AsyncUsersResourceWithStreamingResponse

        return AsyncUsersResourceWithStreamingResponse(self._client.users)

    @cached_property
    def data(self) -> data.AsyncDataResourceWithStreamingResponse:
        from .resources.data import AsyncDataResourceWithStreamingResponse

        return AsyncDataResourceWithStreamingResponse(self._client.data)

    @cached_property
    def health(self) -> health.AsyncHealthResourceWithStreamingResponse:
        from .resources.health import AsyncHealthResourceWithStreamingResponse

        return AsyncHealthResourceWithStreamingResponse(self._client.health)

    @cached_property
    def auth(self) -> auth.AsyncAuthResourceWithStreamingResponse:
        from .resources.auth import AsyncAuthResourceWithStreamingResponse

        return AsyncAuthResourceWithStreamingResponse(self._client.auth)

    @cached_property
    def personas(self) -> personas.AsyncPersonasResourceWithStreamingResponse:
        from .resources.personas import AsyncPersonasResourceWithStreamingResponse

        return AsyncPersonasResourceWithStreamingResponse(self._client.personas)

    @cached_property
    def inference(self) -> inference.AsyncInferenceResourceWithStreamingResponse:
        from .resources.inference import AsyncInferenceResourceWithStreamingResponse

        return AsyncInferenceResourceWithStreamingResponse(self._client.inference)

    @cached_property
    def demo(self) -> demo.AsyncDemoResourceWithStreamingResponse:
        from .resources.demo import AsyncDemoResourceWithStreamingResponse

        return AsyncDemoResourceWithStreamingResponse(self._client.demo)


Client = ElicitClient

AsyncClient = AsyncElicitClient
