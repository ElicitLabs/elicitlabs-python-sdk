# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..types import (
    project_list_params,
    project_clone_params,
    project_create_params,
    project_delete_params,
    project_retrieve_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.project_list_response import ProjectListResponse
from ..types.project_clone_response import ProjectCloneResponse
from ..types.project_create_response import ProjectCreateResponse
from ..types.project_delete_response import ProjectDeleteResponse
from ..types.project_retrieve_response import ProjectRetrieveResponse

__all__ = ["ProjectsResource", "AsyncProjectsResource"]


class ProjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ProjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return ProjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ProjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return ProjectsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        project_type: Literal["creative_design", "general"] | Omit = omit,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectCreateResponse:
        """
        Create a new project for a user.

            This endpoint:
            - Creates a new project with the provided name and description
            - Associates the project with the specified user_id, or the authenticated user if not provided
            - The project will have access to user's preferences, episodes, and identity
            - Returns the created project with all metadata

            **Authentication**: Requires valid API key or JWT token

        Args:
          name: Project name

          description: Optional project description

          project_type: Project type override. When set, skips LLM classification during content
              ingestion. Use 'creative_design' for artistic/design projects, 'general' for
              documentation/business content.

          user_id: User ID to associate the project with. If not provided, uses the authenticated
              user's ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/projects",
            body=maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "project_type": project_type,
                    "user_id": user_id,
                },
                project_create_params.ProjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProjectCreateResponse,
        )

    def retrieve(
        self,
        project_id: str,
        *,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectRetrieveResponse:
        """
        Retrieve details of a specific project by its unique identifier.

            This endpoint:
            - Returns full project information including metadata
            - Includes user information for the project owner
            - Verifies the authenticated user owns the project or belongs to the same org
            - Returns 404 if project is not found

            **Authentication**: Requires valid API key or JWT token in Authorization header

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._get(
            path_template("/v1/projects/{project_id}", project_id=project_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"user_id": user_id}, project_retrieve_params.ProjectRetrieveParams),
            ),
            cast_to=ProjectRetrieveResponse,
        )

    def list(
        self,
        *,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectListResponse:
        """
        Get projects accessible to the caller.

            This endpoint:
            - **No user_id param** (or user_id == root user): root user → returns **all** projects across the org
            - **user_id param** (sub-user): returns only that sub-user's projects
            - Includes project metadata (name, description, creation date)

            **Authentication**: Requires valid API key or JWT token

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/projects",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"user_id": user_id}, project_list_params.ProjectListParams),
            ),
            cast_to=ProjectListResponse,
        )

    def delete(
        self,
        project_id: str,
        *,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectDeleteResponse:
        """
        Delete a project by its ID.

            This endpoint:
            - Permanently deletes the project
            - Verifies the authenticated user owns the project
            - Returns confirmation of deletion

            **Note**: This action cannot be undone.

            **Authentication**: Requires valid API key or JWT token

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return self._delete(
            path_template("/v1/projects/{project_id}", project_id=project_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"user_id": user_id}, project_delete_params.ProjectDeleteParams),
            ),
            cast_to=ProjectDeleteResponse,
        )

    def clone(
        self,
        *,
        project_id: str,
        description: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        source_user_id: str | Omit = omit,
        target_user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectCloneResponse:
        """
        Deep-clone a project, including all its Neo4j memory graph data and referenced
        GCS assets, into a new independent project.

            This endpoint:
            - Creates a new project in PostgreSQL with the source project's metadata
            - Copies all GCS files (images, objects) under a new project path
            - Deep-copies all Neo4j nodes (episodes, entities, preferences, identity,
              hierarchical data, multimodal nodes) with new UUIDs
            - Rewrites GCS URLs in ImageNode/ObjectNode to point at the copied files
            - Recreates all inter-node relationships

            The clone is fully independent — changes to one project do not affect the other.

            **Authentication**: Requires valid API key or JWT token

        Args:
          project_id: ID of the project to clone

          description: Description for the cloned project. Defaults to the original's description.

          name: Name for the cloned project. Defaults to '{original_name} (Copy)'.

          source_user_id: User ID of the source project owner. If not provided, uses the authenticated
              user's ID.

          target_user_id: Target user ID to own the cloned project. If not provided, uses the
              authenticated user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/projects/clone",
            body=maybe_transform(
                {
                    "project_id": project_id,
                    "description": description,
                    "name": name,
                    "source_user_id": source_user_id,
                    "target_user_id": target_user_id,
                },
                project_clone_params.ProjectCloneParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProjectCloneResponse,
        )


class AsyncProjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncProjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#accessing-raw-response-data-eg-headers
        """
        return AsyncProjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncProjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ElicitLabs/elicitlabs-python-sdk#with_streaming_response
        """
        return AsyncProjectsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        description: Optional[str] | Omit = omit,
        project_type: Literal["creative_design", "general"] | Omit = omit,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectCreateResponse:
        """
        Create a new project for a user.

            This endpoint:
            - Creates a new project with the provided name and description
            - Associates the project with the specified user_id, or the authenticated user if not provided
            - The project will have access to user's preferences, episodes, and identity
            - Returns the created project with all metadata

            **Authentication**: Requires valid API key or JWT token

        Args:
          name: Project name

          description: Optional project description

          project_type: Project type override. When set, skips LLM classification during content
              ingestion. Use 'creative_design' for artistic/design projects, 'general' for
              documentation/business content.

          user_id: User ID to associate the project with. If not provided, uses the authenticated
              user's ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/projects",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "description": description,
                    "project_type": project_type,
                    "user_id": user_id,
                },
                project_create_params.ProjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProjectCreateResponse,
        )

    async def retrieve(
        self,
        project_id: str,
        *,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectRetrieveResponse:
        """
        Retrieve details of a specific project by its unique identifier.

            This endpoint:
            - Returns full project information including metadata
            - Includes user information for the project owner
            - Verifies the authenticated user owns the project or belongs to the same org
            - Returns 404 if project is not found

            **Authentication**: Requires valid API key or JWT token in Authorization header

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._get(
            path_template("/v1/projects/{project_id}", project_id=project_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"user_id": user_id}, project_retrieve_params.ProjectRetrieveParams),
            ),
            cast_to=ProjectRetrieveResponse,
        )

    async def list(
        self,
        *,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectListResponse:
        """
        Get projects accessible to the caller.

            This endpoint:
            - **No user_id param** (or user_id == root user): root user → returns **all** projects across the org
            - **user_id param** (sub-user): returns only that sub-user's projects
            - Includes project metadata (name, description, creation date)

            **Authentication**: Requires valid API key or JWT token

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/projects",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"user_id": user_id}, project_list_params.ProjectListParams),
            ),
            cast_to=ProjectListResponse,
        )

    async def delete(
        self,
        project_id: str,
        *,
        user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectDeleteResponse:
        """
        Delete a project by its ID.

            This endpoint:
            - Permanently deletes the project
            - Verifies the authenticated user owns the project
            - Returns confirmation of deletion

            **Note**: This action cannot be undone.

            **Authentication**: Requires valid API key or JWT token

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not project_id:
            raise ValueError(f"Expected a non-empty value for `project_id` but received {project_id!r}")
        return await self._delete(
            path_template("/v1/projects/{project_id}", project_id=project_id),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"user_id": user_id}, project_delete_params.ProjectDeleteParams),
            ),
            cast_to=ProjectDeleteResponse,
        )

    async def clone(
        self,
        *,
        project_id: str,
        description: Optional[str] | Omit = omit,
        name: Optional[str] | Omit = omit,
        source_user_id: str | Omit = omit,
        target_user_id: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ProjectCloneResponse:
        """
        Deep-clone a project, including all its Neo4j memory graph data and referenced
        GCS assets, into a new independent project.

            This endpoint:
            - Creates a new project in PostgreSQL with the source project's metadata
            - Copies all GCS files (images, objects) under a new project path
            - Deep-copies all Neo4j nodes (episodes, entities, preferences, identity,
              hierarchical data, multimodal nodes) with new UUIDs
            - Rewrites GCS URLs in ImageNode/ObjectNode to point at the copied files
            - Recreates all inter-node relationships

            The clone is fully independent — changes to one project do not affect the other.

            **Authentication**: Requires valid API key or JWT token

        Args:
          project_id: ID of the project to clone

          description: Description for the cloned project. Defaults to the original's description.

          name: Name for the cloned project. Defaults to '{original_name} (Copy)'.

          source_user_id: User ID of the source project owner. If not provided, uses the authenticated
              user's ID.

          target_user_id: Target user ID to own the cloned project. If not provided, uses the
              authenticated user.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/projects/clone",
            body=await async_maybe_transform(
                {
                    "project_id": project_id,
                    "description": description,
                    "name": name,
                    "source_user_id": source_user_id,
                    "target_user_id": target_user_id,
                },
                project_clone_params.ProjectCloneParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ProjectCloneResponse,
        )


class ProjectsResourceWithRawResponse:
    def __init__(self, projects: ProjectsResource) -> None:
        self._projects = projects

        self.create = to_raw_response_wrapper(
            projects.create,
        )
        self.retrieve = to_raw_response_wrapper(
            projects.retrieve,
        )
        self.list = to_raw_response_wrapper(
            projects.list,
        )
        self.delete = to_raw_response_wrapper(
            projects.delete,
        )
        self.clone = to_raw_response_wrapper(
            projects.clone,
        )


class AsyncProjectsResourceWithRawResponse:
    def __init__(self, projects: AsyncProjectsResource) -> None:
        self._projects = projects

        self.create = async_to_raw_response_wrapper(
            projects.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            projects.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            projects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            projects.delete,
        )
        self.clone = async_to_raw_response_wrapper(
            projects.clone,
        )


class ProjectsResourceWithStreamingResponse:
    def __init__(self, projects: ProjectsResource) -> None:
        self._projects = projects

        self.create = to_streamed_response_wrapper(
            projects.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            projects.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            projects.list,
        )
        self.delete = to_streamed_response_wrapper(
            projects.delete,
        )
        self.clone = to_streamed_response_wrapper(
            projects.clone,
        )


class AsyncProjectsResourceWithStreamingResponse:
    def __init__(self, projects: AsyncProjectsResource) -> None:
        self._projects = projects

        self.create = async_to_streamed_response_wrapper(
            projects.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            projects.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            projects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            projects.delete,
        )
        self.clone = async_to_streamed_response_wrapper(
            projects.clone,
        )
