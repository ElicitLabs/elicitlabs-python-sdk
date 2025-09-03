# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional

import httpx

from ..types import (
    modal_initialize_params,
    modal_analyze_text_params,
    modal_respond_to_query_params,
    modal_generate_autocomplete_params,
    modal_answer_backslash_query_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.app_context_param import AppContextParam
from ..types.modal_initialize_response import ModalInitializeResponse
from ..types.modal_analyze_text_response import ModalAnalyzeTextResponse
from ..types.modal_respond_to_query_response import ModalRespondToQueryResponse
from ..types.modal_generate_autocomplete_response import ModalGenerateAutocompleteResponse
from ..types.modal_answer_backslash_query_response import ModalAnswerBackslashQueryResponse

__all__ = ["ModalResource", "AsyncModalResource"]


class ModalResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ModalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/elicit-labs-python#accessing-raw-response-data-eg-headers
        """
        return ModalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ModalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/elicit-labs-python#with_streaming_response
        """
        return ModalResourceWithStreamingResponse(self)

    def analyze_text(
        self,
        *,
        text_to_analyze: str,
        user_id: str,
        conversation_history: Optional[Iterable[Dict[str, object]]] | NotGiven = NOT_GIVEN,
        document_type: str | NotGiven = NOT_GIVEN,
        session_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalAnalyzeTextResponse:
        """
        Analyze text quality and provide detailed feedback on typos, grammar, style, and
        other improvements.

            This endpoint:
            - Analyzes text for typos, spelling errors, and grammar issues
            - Provides specific suggestions with severity levels (low/medium/high)
            - Offers style and clarity improvements based on document type
            - Returns corrected text with all improvements applied
            - Considers user context and preferences for personalized feedback

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          text_to_analyze: The text to analyze for quality improvements

          user_id: Unique identifier for the user

          conversation_history: Recent conversation messages for context

          document_type: Type of document being analyzed (email/document)

          session_id: Session identifier for conversation continuity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/modal_reflection",
            body=maybe_transform(
                {
                    "text_to_analyze": text_to_analyze,
                    "user_id": user_id,
                    "conversation_history": conversation_history,
                    "document_type": document_type,
                    "session_id": session_id,
                },
                modal_analyze_text_params.ModalAnalyzeTextParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalAnalyzeTextResponse,
        )

    def answer_backslash_query(
        self,
        *,
        context_text: str,
        query: str,
        user_id: str,
        conversation_history: Optional[Iterable[Dict[str, object]]] | NotGiven = NOT_GIVEN,
        document_type: str | NotGiven = NOT_GIVEN,
        session_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalAnswerBackslashQueryResponse:
        """
        Process backslash Q queries to provide contextual answers that fit perfectly
        within the surrounding text.

            This endpoint:
            - Analyzes the query within its surrounding text context
            - Retrieves relevant user memories and preferences for personalization
            - Generates answers that seamlessly integrate with the existing text
            - Matches tone, style, and formality of the surrounding content
            - Provides confidence scoring and reasoning for the generated answer

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          context_text: The surrounding text context where the answer should fit

          query: The query/question to answer within the context

          user_id: Unique identifier for the user

          conversation_history: Recent conversation messages for context

          document_type: Type of document (email/document)

          session_id: Session identifier for conversation continuity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/modal_backslash_q",
            body=maybe_transform(
                {
                    "context_text": context_text,
                    "query": query,
                    "user_id": user_id,
                    "conversation_history": conversation_history,
                    "document_type": document_type,
                    "session_id": session_id,
                },
                modal_answer_backslash_query_params.ModalAnswerBackslashQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalAnswerBackslashQueryResponse,
        )

    def generate_autocomplete(
        self,
        *,
        partial_text: str,
        user_id: str,
        conversation_history: Optional[Iterable[Dict[str, object]]] | NotGiven = NOT_GIVEN,
        document_type: str | NotGiven = NOT_GIVEN,
        session_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalGenerateAutocompleteResponse:
        """
        Generate intelligent autocomplete suggestions for the modal writing interface
        with advanced caching.

            This endpoint is the core of the modal autocomplete writing software:
            - Analyzes partial user input with intelligent wait/complete decisions
            - Retrieves relevant memories and writing patterns
            - Uses KV caching for optimal performance during frequent typing
            - Returns contextually aware completions with confidence scoring
            - Provides action guidance (complete/wait) based on input analysis

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          partial_text: The partial text input from user to complete

          user_id: Unique identifier for the user

          conversation_history: Recent conversation messages for context

          document_type: Type of document being completed (email/document)

          session_id: Session identifier for conversation continuity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/modal_autocomplete",
            body=maybe_transform(
                {
                    "partial_text": partial_text,
                    "user_id": user_id,
                    "conversation_history": conversation_history,
                    "document_type": document_type,
                    "session_id": session_id,
                },
                modal_generate_autocomplete_params.ModalGenerateAutocompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalGenerateAutocompleteResponse,
        )

    def initialize(
        self,
        *,
        app_context: AppContextParam,
        session_id: str,
        user_id: str,
        screenshot_base64: Optional[str] | NotGiven = NOT_GIVEN,
        screenshot_path: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalInitializeResponse:
        """
        Initialize a new modal writing session with comprehensive context analysis.

            This endpoint:
            - Analyzes screenshots to extract email features and context
            - Retrieves relevant user memories, preferences, and identity attributes
            - Sets up personalized writing context for the modal interface
            - Returns comprehensive session context for optimal writing experience

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          app_context: Application context information

          session_id: Session identifier for conversation continuity

          user_id: Unique identifier for the user

          screenshot_base64: Base64 encoded screenshot for analysis

          screenshot_path: Path to screenshot file for analysis

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/modal_initialization",
            body=maybe_transform(
                {
                    "app_context": app_context,
                    "session_id": session_id,
                    "user_id": user_id,
                    "screenshot_base64": screenshot_base64,
                    "screenshot_path": screenshot_path,
                },
                modal_initialize_params.ModalInitializeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalInitializeResponse,
        )

    def respond_to_query(
        self,
        *,
        message: str,
        session_id: str,
        user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalRespondToQueryResponse:
        """
        Process user queries and provide personalized responses using memory context.

            This endpoint:
            - Retrieves relevant user memories and preferences
            - Processes the user's query with personalized context
            - Generates tailored responses based on user history
            - Returns personalized information relevant to the user

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          message: Single message string to process

          session_id: Session identifier for conversation continuity

          user_id: Unique identifier for the user

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/modal/modal_query",
            body=maybe_transform(
                {
                    "message": message,
                    "session_id": session_id,
                    "user_id": user_id,
                },
                modal_respond_to_query_params.ModalRespondToQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalRespondToQueryResponse,
        )


class AsyncModalResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncModalResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/stainless-sdks/elicit-labs-python#accessing-raw-response-data-eg-headers
        """
        return AsyncModalResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncModalResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/stainless-sdks/elicit-labs-python#with_streaming_response
        """
        return AsyncModalResourceWithStreamingResponse(self)

    async def analyze_text(
        self,
        *,
        text_to_analyze: str,
        user_id: str,
        conversation_history: Optional[Iterable[Dict[str, object]]] | NotGiven = NOT_GIVEN,
        document_type: str | NotGiven = NOT_GIVEN,
        session_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalAnalyzeTextResponse:
        """
        Analyze text quality and provide detailed feedback on typos, grammar, style, and
        other improvements.

            This endpoint:
            - Analyzes text for typos, spelling errors, and grammar issues
            - Provides specific suggestions with severity levels (low/medium/high)
            - Offers style and clarity improvements based on document type
            - Returns corrected text with all improvements applied
            - Considers user context and preferences for personalized feedback

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          text_to_analyze: The text to analyze for quality improvements

          user_id: Unique identifier for the user

          conversation_history: Recent conversation messages for context

          document_type: Type of document being analyzed (email/document)

          session_id: Session identifier for conversation continuity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/modal_reflection",
            body=await async_maybe_transform(
                {
                    "text_to_analyze": text_to_analyze,
                    "user_id": user_id,
                    "conversation_history": conversation_history,
                    "document_type": document_type,
                    "session_id": session_id,
                },
                modal_analyze_text_params.ModalAnalyzeTextParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalAnalyzeTextResponse,
        )

    async def answer_backslash_query(
        self,
        *,
        context_text: str,
        query: str,
        user_id: str,
        conversation_history: Optional[Iterable[Dict[str, object]]] | NotGiven = NOT_GIVEN,
        document_type: str | NotGiven = NOT_GIVEN,
        session_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalAnswerBackslashQueryResponse:
        """
        Process backslash Q queries to provide contextual answers that fit perfectly
        within the surrounding text.

            This endpoint:
            - Analyzes the query within its surrounding text context
            - Retrieves relevant user memories and preferences for personalization
            - Generates answers that seamlessly integrate with the existing text
            - Matches tone, style, and formality of the surrounding content
            - Provides confidence scoring and reasoning for the generated answer

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          context_text: The surrounding text context where the answer should fit

          query: The query/question to answer within the context

          user_id: Unique identifier for the user

          conversation_history: Recent conversation messages for context

          document_type: Type of document (email/document)

          session_id: Session identifier for conversation continuity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/modal_backslash_q",
            body=await async_maybe_transform(
                {
                    "context_text": context_text,
                    "query": query,
                    "user_id": user_id,
                    "conversation_history": conversation_history,
                    "document_type": document_type,
                    "session_id": session_id,
                },
                modal_answer_backslash_query_params.ModalAnswerBackslashQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalAnswerBackslashQueryResponse,
        )

    async def generate_autocomplete(
        self,
        *,
        partial_text: str,
        user_id: str,
        conversation_history: Optional[Iterable[Dict[str, object]]] | NotGiven = NOT_GIVEN,
        document_type: str | NotGiven = NOT_GIVEN,
        session_id: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalGenerateAutocompleteResponse:
        """
        Generate intelligent autocomplete suggestions for the modal writing interface
        with advanced caching.

            This endpoint is the core of the modal autocomplete writing software:
            - Analyzes partial user input with intelligent wait/complete decisions
            - Retrieves relevant memories and writing patterns
            - Uses KV caching for optimal performance during frequent typing
            - Returns contextually aware completions with confidence scoring
            - Provides action guidance (complete/wait) based on input analysis

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          partial_text: The partial text input from user to complete

          user_id: Unique identifier for the user

          conversation_history: Recent conversation messages for context

          document_type: Type of document being completed (email/document)

          session_id: Session identifier for conversation continuity

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/modal_autocomplete",
            body=await async_maybe_transform(
                {
                    "partial_text": partial_text,
                    "user_id": user_id,
                    "conversation_history": conversation_history,
                    "document_type": document_type,
                    "session_id": session_id,
                },
                modal_generate_autocomplete_params.ModalGenerateAutocompleteParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalGenerateAutocompleteResponse,
        )

    async def initialize(
        self,
        *,
        app_context: AppContextParam,
        session_id: str,
        user_id: str,
        screenshot_base64: Optional[str] | NotGiven = NOT_GIVEN,
        screenshot_path: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalInitializeResponse:
        """
        Initialize a new modal writing session with comprehensive context analysis.

            This endpoint:
            - Analyzes screenshots to extract email features and context
            - Retrieves relevant user memories, preferences, and identity attributes
            - Sets up personalized writing context for the modal interface
            - Returns comprehensive session context for optimal writing experience

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          app_context: Application context information

          session_id: Session identifier for conversation continuity

          user_id: Unique identifier for the user

          screenshot_base64: Base64 encoded screenshot for analysis

          screenshot_path: Path to screenshot file for analysis

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/modal_initialization",
            body=await async_maybe_transform(
                {
                    "app_context": app_context,
                    "session_id": session_id,
                    "user_id": user_id,
                    "screenshot_base64": screenshot_base64,
                    "screenshot_path": screenshot_path,
                },
                modal_initialize_params.ModalInitializeParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalInitializeResponse,
        )

    async def respond_to_query(
        self,
        *,
        message: str,
        session_id: str,
        user_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ModalRespondToQueryResponse:
        """
        Process user queries and provide personalized responses using memory context.

            This endpoint:
            - Retrieves relevant user memories and preferences
            - Processes the user's query with personalized context
            - Generates tailored responses based on user history
            - Returns personalized information relevant to the user

            **Authentication**: Requires valid JWT token in Authorization header

        Args:
          message: Single message string to process

          session_id: Session identifier for conversation continuity

          user_id: Unique identifier for the user

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/modal/modal_query",
            body=await async_maybe_transform(
                {
                    "message": message,
                    "session_id": session_id,
                    "user_id": user_id,
                },
                modal_respond_to_query_params.ModalRespondToQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ModalRespondToQueryResponse,
        )


class ModalResourceWithRawResponse:
    def __init__(self, modal: ModalResource) -> None:
        self._modal = modal

        self.analyze_text = to_raw_response_wrapper(
            modal.analyze_text,
        )
        self.answer_backslash_query = to_raw_response_wrapper(
            modal.answer_backslash_query,
        )
        self.generate_autocomplete = to_raw_response_wrapper(
            modal.generate_autocomplete,
        )
        self.initialize = to_raw_response_wrapper(
            modal.initialize,
        )
        self.respond_to_query = to_raw_response_wrapper(
            modal.respond_to_query,
        )


class AsyncModalResourceWithRawResponse:
    def __init__(self, modal: AsyncModalResource) -> None:
        self._modal = modal

        self.analyze_text = async_to_raw_response_wrapper(
            modal.analyze_text,
        )
        self.answer_backslash_query = async_to_raw_response_wrapper(
            modal.answer_backslash_query,
        )
        self.generate_autocomplete = async_to_raw_response_wrapper(
            modal.generate_autocomplete,
        )
        self.initialize = async_to_raw_response_wrapper(
            modal.initialize,
        )
        self.respond_to_query = async_to_raw_response_wrapper(
            modal.respond_to_query,
        )


class ModalResourceWithStreamingResponse:
    def __init__(self, modal: ModalResource) -> None:
        self._modal = modal

        self.analyze_text = to_streamed_response_wrapper(
            modal.analyze_text,
        )
        self.answer_backslash_query = to_streamed_response_wrapper(
            modal.answer_backslash_query,
        )
        self.generate_autocomplete = to_streamed_response_wrapper(
            modal.generate_autocomplete,
        )
        self.initialize = to_streamed_response_wrapper(
            modal.initialize,
        )
        self.respond_to_query = to_streamed_response_wrapper(
            modal.respond_to_query,
        )


class AsyncModalResourceWithStreamingResponse:
    def __init__(self, modal: AsyncModalResource) -> None:
        self._modal = modal

        self.analyze_text = async_to_streamed_response_wrapper(
            modal.analyze_text,
        )
        self.answer_backslash_query = async_to_streamed_response_wrapper(
            modal.answer_backslash_query,
        )
        self.generate_autocomplete = async_to_streamed_response_wrapper(
            modal.generate_autocomplete,
        )
        self.initialize = async_to_streamed_response_wrapper(
            modal.initialize,
        )
        self.respond_to_query = async_to_streamed_response_wrapper(
            modal.respond_to_query,
        )
