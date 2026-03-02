from __future__ import annotations

import os
from typing import Optional

from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from .session import AsyncRealtimeSession

__all__ = ["RealtimeResource", "AsyncRealtimeResource"]


class RealtimeResource(SyncAPIResource):
    """Realtime gateway resource (sync client).

    WebSocket sessions are inherently asynchronous. Use
    :class:`AsyncElicitClient` with ``client.realtime.connect()``
    for full realtime support.
    """

    @cached_property
    def with_raw_response(self) -> RealtimeResourceWithRawResponse:
        return RealtimeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RealtimeResourceWithStreamingResponse:
        return RealtimeResourceWithStreamingResponse(self)

    def connect(
        self,
        *,
        session_id: str,
        user_id: str,
        generation: bool = True,
        gateway_url: Optional[str] = None,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        disabled_learning: bool = False,
        auto_listen: bool = True,
    ) -> AsyncRealtimeSession:
        """Create a realtime session context manager.

        Although this is on the sync client, the returned session is async
        and must be used with ``async with``::

            session = client.realtime.connect(
                session_id="my-session",
                user_id="my-user",
                generation=False,
            )
            async with session:
                await session.send_audio(pcm_data)
                async for event in session:
                    print(event)

        Args:
            session_id: Unique session identifier.
            user_id: The end-user ID.
            generation: If ``False``, the gateway runs perception + retrieval
                only — no LLM generation. You receive ``context_update``
                events and use them in your own LLM calls.
            gateway_url: Override the gateway WebSocket URL.
                Defaults to ``wss://gateway.elicitlabs.ai/ws``
                or the ``ELICIT_GATEWAY_URL`` environment variable.
            project_id: Optional project scope.
            persona_id: Optional persona scope.
            disabled_learning: Disable memory learning for this session.
            auto_listen: If ``True`` (default), a background task reads
                events and accumulates context automatically. Use
                :meth:`~AsyncRealtimeSession.flush` to retrieve data.
                If ``False``, no background listener is started — use
                ``async for event in session`` or :meth:`~AsyncRealtimeSession.recv`
                to consume events manually.
        """
        url = gateway_url or os.environ.get("ELICIT_GATEWAY_URL")
        return AsyncRealtimeSession(
            api_key=self._client.api_key,
            user_id=user_id,
            session_id=session_id,
            generation=generation,
            gateway_url=url,
            project_id=project_id,
            persona_id=persona_id,
            disabled_learning=disabled_learning,
            auto_listen=auto_listen,
        )


class AsyncRealtimeResource(AsyncAPIResource):
    """Realtime gateway resource for the async client.

    Use :meth:`connect` to create a WebSocket session::

        async with client.realtime.connect(
            session_id="my-session",
            user_id="my-user",
            generation=False,
        ) as session:
            await session.send_audio(pcm_data)
            async for event in session:
                print(event)
    """

    @cached_property
    def with_raw_response(self) -> AsyncRealtimeResourceWithRawResponse:
        return AsyncRealtimeResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRealtimeResourceWithStreamingResponse:
        return AsyncRealtimeResourceWithStreamingResponse(self)

    def connect(
        self,
        *,
        session_id: str,
        user_id: str,
        generation: bool = True,
        gateway_url: Optional[str] = None,
        project_id: Optional[str] = None,
        persona_id: Optional[str] = None,
        disabled_learning: bool = False,
        auto_listen: bool = True,
    ) -> AsyncRealtimeSession:
        """Create a realtime session context manager.

        Returns an :class:`~elicitlabs.resources.realtime.session.AsyncRealtimeSession`
        that is used as an async context manager::

            async with client.realtime.connect(
                session_id="my-session",
                user_id="my-user",
                generation=False,
            ) as session:
                await session.send_audio(pcm_data)
                async for event in session:
                    if event.type == "context_update":
                        print(session.context.build_context_string())

        Args:
            session_id: Unique session identifier.
            user_id: The end-user ID.
            generation: If ``False``, the gateway runs perception + retrieval
                only — no LLM generation. You receive ``context_update``
                events and use them in your own LLM calls.
            gateway_url: Override the gateway WebSocket URL.
                Defaults to ``wss://gateway.elicitlabs.ai/ws``
                or the ``ELICIT_GATEWAY_URL`` environment variable.
            project_id: Optional project scope.
            persona_id: Optional persona scope.
            disabled_learning: Disable memory learning for this session.
            auto_listen: If ``True`` (default), a background task reads
                events and accumulates context automatically. Use
                :meth:`~AsyncRealtimeSession.flush` to retrieve data.
                If ``False``, no background listener is started — use
                ``async for event in session`` or :meth:`~AsyncRealtimeSession.recv`
                to consume events manually.
        """
        url = gateway_url or os.environ.get("ELICIT_GATEWAY_URL")
        return AsyncRealtimeSession(
            api_key=self._client.api_key,
            user_id=user_id,
            session_id=session_id,
            generation=generation,
            gateway_url=url,
            project_id=project_id,
            persona_id=persona_id,
            disabled_learning=disabled_learning,
            auto_listen=auto_listen,
        )


class RealtimeResourceWithRawResponse:
    def __init__(self, realtime: RealtimeResource) -> None:
        self._realtime = realtime


class AsyncRealtimeResourceWithRawResponse:
    def __init__(self, realtime: AsyncRealtimeResource) -> None:
        self._realtime = realtime


class RealtimeResourceWithStreamingResponse:
    def __init__(self, realtime: RealtimeResource) -> None:
        self._realtime = realtime


class AsyncRealtimeResourceWithStreamingResponse:
    def __init__(self, realtime: AsyncRealtimeResource) -> None:
        self._realtime = realtime
