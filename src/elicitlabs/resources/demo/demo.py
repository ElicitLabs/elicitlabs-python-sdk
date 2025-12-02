# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional

import httpx

from .org import (
    OrgResource,
    AsyncOrgResource,
    OrgResourceWithRawResponse,
    AsyncOrgResourceWithRawResponse,
    OrgResourceWithStreamingResponse,
    AsyncOrgResourceWithStreamingResponse,
)
from .auth import (
    AuthResource,
    AsyncAuthResource,
    AuthResourceWithRawResponse,
    AsyncAuthResourceWithRawResponse,
    AuthResourceWithStreamingResponse,
    AsyncAuthResourceWithStreamingResponse,
)
from ...types import (
    demo_sign_in_params,
    demo_create_user_params,
    demo_reset_password_params,
    demo_generate_reset_link_params,
    demo_request_password_reset_params,
    demo_submit_early_access_request_params,
)
from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.demo_sign_in_response import DemoSignInResponse
from ...types.demo_create_user_response import DemoCreateUserResponse
from ...types.demo_reset_password_response import DemoResetPasswordResponse
from ...types.demo_generate_reset_link_response import DemoGenerateResetLinkResponse
from ...types.demo_retrieve_current_user_response import DemoRetrieveCurrentUserResponse
from ...types.demo_request_password_reset_response import DemoRequestPasswordResetResponse
from ...types.demo_submit_early_access_request_response import DemoSubmitEarlyAccessRequestResponse

__all__ = ["DemoResource", "AsyncDemoResource"]


class DemoResource(SyncAPIResource):
    @cached_property
    def auth(self) -> AuthResource:
        return AuthResource(self._client)

    @cached_property
    def org(self) -> OrgResource:
        return OrgResource(self._client)

    @cached_property
    def with_raw_response(self) -> DemoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return DemoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DemoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return DemoResourceWithStreamingResponse(self)

    def create_user(
        self,
        *,
        email: str,
        name: str,
        password: str,
        org_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoCreateUserResponse:
        """
        Create a new user account and return JWT authentication token.

            This endpoint:
            - Creates a new user with email and password
            - Automatically creates a default organization if not provided
            - Generates JWT authentication token
            - Sends welcome email to the new user
            - Returns user information and access token

            **Authentication**: No authentication required

        Args:
          email: User's email address

          name: User's full name

          password: User's password (minimum 6 characters)

          org_id: Optional organization ID. If not provided, a default organization will be
              created automatically with the format 'Org: {user_name}'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/demo/signup",
            body=maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "password": password,
                    "org_id": org_id,
                },
                demo_create_user_params.DemoCreateUserParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoCreateUserResponse,
        )

    def generate_reset_link(
        self,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoGenerateResetLinkResponse:
        """
        Generate password reset link for a user (for testing or admin purposes).

            This endpoint:
            - Generates password reset token and URL
            - Returns the full reset link
            - Token expires after 1 hour
            - Useful for testing or admin tools

            **Authentication**: No authentication required

        Args:
          email: User's email address

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/demo/get-reset-link",
            body=maybe_transform({"email": email}, demo_generate_reset_link_params.DemoGenerateResetLinkParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoGenerateResetLinkResponse,
        )

    def request_password_reset(
        self,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoRequestPasswordResetResponse:
        """
        Send password reset email to user's email address.

            This endpoint:
            - Generates password reset token
            - Sends reset link via email
            - Token expires after 1 hour
            - Returns generic success message for security

            **Authentication**: No authentication required

        Args:
          email: User's email address

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/demo/forgot-password",
            body=maybe_transform({"email": email}, demo_request_password_reset_params.DemoRequestPasswordResetParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoRequestPasswordResetResponse,
        )

    def reset_password(
        self,
        *,
        token: str,
        confirm_password: str,
        new_password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoResetPasswordResponse:
        """
        Reset user password using the token from password reset email.

            This endpoint:
            - Verifies the reset token validity
            - Updates user password
            - Sends password changed notification email
            - Invalidates the reset token after use

            **Authentication**: Requires valid reset token (no user authentication)

        Args:
          token: Password reset token

          confirm_password: Confirmation of new password

          new_password: New password (minimum 6 characters)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/demo/reset-password",
            body=maybe_transform(
                {
                    "token": token,
                    "confirm_password": confirm_password,
                    "new_password": new_password,
                },
                demo_reset_password_params.DemoResetPasswordParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoResetPasswordResponse,
        )

    def retrieve_current_user(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoRetrieveCurrentUserResponse:
        """
        Retrieve information about the currently authenticated user.

            This endpoint:
            - Returns user profile information
            - Includes organization details
            - Requires valid JWT token

            **Authentication**: Requires valid JWT token in Authorization header
        """
        return self._get(
            "/v1/demo/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoRetrieveCurrentUserResponse,
        )

    def sign_in(
        self,
        *,
        email: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoSignInResponse:
        """
        Authenticate user with email and password and return JWT token.

            This endpoint:
            - Validates user credentials (email and password)
            - Generates JWT authentication token
            - Returns user information and access token
            - Token expires after 24 hours

            **Authentication**: No authentication required

        Args:
          email: User's email address

          password: User's password

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/demo/signin",
            body=maybe_transform(
                {
                    "email": email,
                    "password": password,
                },
                demo_sign_in_params.DemoSignInParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoSignInResponse,
        )

    def submit_early_access_request(
        self,
        *,
        email: str,
        name: str,
        company_size: Optional[str] | Omit = omit,
        industry: Optional[str] | Omit = omit,
        role: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoSubmitEarlyAccessRequestResponse:
        """
        Submit an early access request for the platform.

            This endpoint:
            - Accepts user information for early access
            - Stores the submission in the database
            - Returns confirmation with submission details
            - Prevents duplicate submissions by email

            **Note**: Each email address can only submit once.

        Args:
          email: User's email address

          name: User's full name

          company_size: Company size range

          industry: User's industry

          role: User's role/job title

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/demo/early-access",
            body=maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "company_size": company_size,
                    "industry": industry,
                    "role": role,
                },
                demo_submit_early_access_request_params.DemoSubmitEarlyAccessRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoSubmitEarlyAccessRequestResponse,
        )


class AsyncDemoResource(AsyncAPIResource):
    @cached_property
    def auth(self) -> AsyncAuthResource:
        return AsyncAuthResource(self._client)

    @cached_property
    def org(self) -> AsyncOrgResource:
        return AsyncOrgResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDemoResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncDemoResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDemoResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncDemoResourceWithStreamingResponse(self)

    async def create_user(
        self,
        *,
        email: str,
        name: str,
        password: str,
        org_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoCreateUserResponse:
        """
        Create a new user account and return JWT authentication token.

            This endpoint:
            - Creates a new user with email and password
            - Automatically creates a default organization if not provided
            - Generates JWT authentication token
            - Sends welcome email to the new user
            - Returns user information and access token

            **Authentication**: No authentication required

        Args:
          email: User's email address

          name: User's full name

          password: User's password (minimum 6 characters)

          org_id: Optional organization ID. If not provided, a default organization will be
              created automatically with the format 'Org: {user_name}'

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/demo/signup",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "password": password,
                    "org_id": org_id,
                },
                demo_create_user_params.DemoCreateUserParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoCreateUserResponse,
        )

    async def generate_reset_link(
        self,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoGenerateResetLinkResponse:
        """
        Generate password reset link for a user (for testing or admin purposes).

            This endpoint:
            - Generates password reset token and URL
            - Returns the full reset link
            - Token expires after 1 hour
            - Useful for testing or admin tools

            **Authentication**: No authentication required

        Args:
          email: User's email address

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/demo/get-reset-link",
            body=await async_maybe_transform(
                {"email": email}, demo_generate_reset_link_params.DemoGenerateResetLinkParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoGenerateResetLinkResponse,
        )

    async def request_password_reset(
        self,
        *,
        email: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoRequestPasswordResetResponse:
        """
        Send password reset email to user's email address.

            This endpoint:
            - Generates password reset token
            - Sends reset link via email
            - Token expires after 1 hour
            - Returns generic success message for security

            **Authentication**: No authentication required

        Args:
          email: User's email address

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/demo/forgot-password",
            body=await async_maybe_transform(
                {"email": email}, demo_request_password_reset_params.DemoRequestPasswordResetParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoRequestPasswordResetResponse,
        )

    async def reset_password(
        self,
        *,
        token: str,
        confirm_password: str,
        new_password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoResetPasswordResponse:
        """
        Reset user password using the token from password reset email.

            This endpoint:
            - Verifies the reset token validity
            - Updates user password
            - Sends password changed notification email
            - Invalidates the reset token after use

            **Authentication**: Requires valid reset token (no user authentication)

        Args:
          token: Password reset token

          confirm_password: Confirmation of new password

          new_password: New password (minimum 6 characters)

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/demo/reset-password",
            body=await async_maybe_transform(
                {
                    "token": token,
                    "confirm_password": confirm_password,
                    "new_password": new_password,
                },
                demo_reset_password_params.DemoResetPasswordParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoResetPasswordResponse,
        )

    async def retrieve_current_user(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoRetrieveCurrentUserResponse:
        """
        Retrieve information about the currently authenticated user.

            This endpoint:
            - Returns user profile information
            - Includes organization details
            - Requires valid JWT token

            **Authentication**: Requires valid JWT token in Authorization header
        """
        return await self._get(
            "/v1/demo/me",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoRetrieveCurrentUserResponse,
        )

    async def sign_in(
        self,
        *,
        email: str,
        password: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoSignInResponse:
        """
        Authenticate user with email and password and return JWT token.

            This endpoint:
            - Validates user credentials (email and password)
            - Generates JWT authentication token
            - Returns user information and access token
            - Token expires after 24 hours

            **Authentication**: No authentication required

        Args:
          email: User's email address

          password: User's password

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/demo/signin",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "password": password,
                },
                demo_sign_in_params.DemoSignInParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoSignInResponse,
        )

    async def submit_early_access_request(
        self,
        *,
        email: str,
        name: str,
        company_size: Optional[str] | Omit = omit,
        industry: Optional[str] | Omit = omit,
        role: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> DemoSubmitEarlyAccessRequestResponse:
        """
        Submit an early access request for the platform.

            This endpoint:
            - Accepts user information for early access
            - Stores the submission in the database
            - Returns confirmation with submission details
            - Prevents duplicate submissions by email

            **Note**: Each email address can only submit once.

        Args:
          email: User's email address

          name: User's full name

          company_size: Company size range

          industry: User's industry

          role: User's role/job title

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/demo/early-access",
            body=await async_maybe_transform(
                {
                    "email": email,
                    "name": name,
                    "company_size": company_size,
                    "industry": industry,
                    "role": role,
                },
                demo_submit_early_access_request_params.DemoSubmitEarlyAccessRequestParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=DemoSubmitEarlyAccessRequestResponse,
        )


class DemoResourceWithRawResponse:
    def __init__(self, demo: DemoResource) -> None:
        self._demo = demo

        self.create_user = to_raw_response_wrapper(
            demo.create_user,
        )
        self.generate_reset_link = to_raw_response_wrapper(
            demo.generate_reset_link,
        )
        self.request_password_reset = to_raw_response_wrapper(
            demo.request_password_reset,
        )
        self.reset_password = to_raw_response_wrapper(
            demo.reset_password,
        )
        self.retrieve_current_user = to_raw_response_wrapper(
            demo.retrieve_current_user,
        )
        self.sign_in = to_raw_response_wrapper(
            demo.sign_in,
        )
        self.submit_early_access_request = to_raw_response_wrapper(
            demo.submit_early_access_request,
        )

    @cached_property
    def auth(self) -> AuthResourceWithRawResponse:
        return AuthResourceWithRawResponse(self._demo.auth)

    @cached_property
    def org(self) -> OrgResourceWithRawResponse:
        return OrgResourceWithRawResponse(self._demo.org)


class AsyncDemoResourceWithRawResponse:
    def __init__(self, demo: AsyncDemoResource) -> None:
        self._demo = demo

        self.create_user = async_to_raw_response_wrapper(
            demo.create_user,
        )
        self.generate_reset_link = async_to_raw_response_wrapper(
            demo.generate_reset_link,
        )
        self.request_password_reset = async_to_raw_response_wrapper(
            demo.request_password_reset,
        )
        self.reset_password = async_to_raw_response_wrapper(
            demo.reset_password,
        )
        self.retrieve_current_user = async_to_raw_response_wrapper(
            demo.retrieve_current_user,
        )
        self.sign_in = async_to_raw_response_wrapper(
            demo.sign_in,
        )
        self.submit_early_access_request = async_to_raw_response_wrapper(
            demo.submit_early_access_request,
        )

    @cached_property
    def auth(self) -> AsyncAuthResourceWithRawResponse:
        return AsyncAuthResourceWithRawResponse(self._demo.auth)

    @cached_property
    def org(self) -> AsyncOrgResourceWithRawResponse:
        return AsyncOrgResourceWithRawResponse(self._demo.org)


class DemoResourceWithStreamingResponse:
    def __init__(self, demo: DemoResource) -> None:
        self._demo = demo

        self.create_user = to_streamed_response_wrapper(
            demo.create_user,
        )
        self.generate_reset_link = to_streamed_response_wrapper(
            demo.generate_reset_link,
        )
        self.request_password_reset = to_streamed_response_wrapper(
            demo.request_password_reset,
        )
        self.reset_password = to_streamed_response_wrapper(
            demo.reset_password,
        )
        self.retrieve_current_user = to_streamed_response_wrapper(
            demo.retrieve_current_user,
        )
        self.sign_in = to_streamed_response_wrapper(
            demo.sign_in,
        )
        self.submit_early_access_request = to_streamed_response_wrapper(
            demo.submit_early_access_request,
        )

    @cached_property
    def auth(self) -> AuthResourceWithStreamingResponse:
        return AuthResourceWithStreamingResponse(self._demo.auth)

    @cached_property
    def org(self) -> OrgResourceWithStreamingResponse:
        return OrgResourceWithStreamingResponse(self._demo.org)


class AsyncDemoResourceWithStreamingResponse:
    def __init__(self, demo: AsyncDemoResource) -> None:
        self._demo = demo

        self.create_user = async_to_streamed_response_wrapper(
            demo.create_user,
        )
        self.generate_reset_link = async_to_streamed_response_wrapper(
            demo.generate_reset_link,
        )
        self.request_password_reset = async_to_streamed_response_wrapper(
            demo.request_password_reset,
        )
        self.reset_password = async_to_streamed_response_wrapper(
            demo.reset_password,
        )
        self.retrieve_current_user = async_to_streamed_response_wrapper(
            demo.retrieve_current_user,
        )
        self.sign_in = async_to_streamed_response_wrapper(
            demo.sign_in,
        )
        self.submit_early_access_request = async_to_streamed_response_wrapper(
            demo.submit_early_access_request,
        )

    @cached_property
    def auth(self) -> AsyncAuthResourceWithStreamingResponse:
        return AsyncAuthResourceWithStreamingResponse(self._demo.auth)

    @cached_property
    def org(self) -> AsyncOrgResourceWithStreamingResponse:
        return AsyncOrgResourceWithStreamingResponse(self._demo.org)
