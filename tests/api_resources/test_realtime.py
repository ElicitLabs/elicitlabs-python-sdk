from __future__ import annotations

import json
import asyncio
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from elicitlabs import ElicitClient, AsyncElicitClient
from elicitlabs.resources.realtime.session import (
    FRAME_AUDIO,
    FRAME_VIDEO,
    _parse_event,
    AsyncRealtimeSession,
    ContextAccumulator,
)
from elicitlabs.types.realtime import (
    ContextCard,
    ErrorEvent,
    TranscriptEvent,
    SessionReadyEvent,
    SessionEndedEvent,
    ContextUpdateEvent,
    ContextCardOperation,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

API_KEY = "upl_test_key"


@pytest.fixture()
def client() -> ElicitClient:
    return ElicitClient(api_key=API_KEY, base_url="http://localhost:4010")


@pytest.fixture()
def async_client() -> AsyncElicitClient:
    return AsyncElicitClient(api_key=API_KEY, base_url="http://localhost:4010")


# ---------------------------------------------------------------------------
# Resource accessibility
# ---------------------------------------------------------------------------


class TestRealtimeResourceAccess:
    def test_sync_client_has_realtime(self, client: ElicitClient) -> None:
        assert hasattr(client, "realtime")
        assert client.realtime is not None

    def test_async_client_has_realtime(self, async_client: AsyncElicitClient) -> None:
        assert hasattr(async_client, "realtime")
        assert async_client.realtime is not None

    def test_sync_connect_returns_session(self, client: ElicitClient) -> None:
        session = client.realtime.connect(
            session_id="s1",
            user_id="u1",
            generation=False,
        )
        assert isinstance(session, AsyncRealtimeSession)

    def test_async_connect_returns_session(self, async_client: AsyncElicitClient) -> None:
        session = async_client.realtime.connect(
            session_id="s1",
            user_id="u1",
            generation=False,
        )
        assert isinstance(session, AsyncRealtimeSession)

    def test_connect_passes_all_params(self, async_client: AsyncElicitClient) -> None:
        session = async_client.realtime.connect(
            session_id="sess-42",
            user_id="user-7",
            generation=False,
            gateway_url="wss://custom.gateway/ws",
            project_id="proj_ABC",
            persona_id="persona_XYZ",
            disabled_learning=True,
        )
        assert session._init_session_id == "sess-42"
        assert session._user_id == "user-7"
        assert session._generation is False
        assert session._gateway_url == "wss://custom.gateway/ws"
        assert session._project_id == "proj_ABC"
        assert session._persona_id == "persona_XYZ"
        assert session._disabled_learning is True

    def test_connect_default_gateway_url(self, async_client: AsyncElicitClient) -> None:
        session = async_client.realtime.connect(
            session_id="s1",
            user_id="u1",
        )
        assert session._gateway_url == "wss://gateway.elicitlabs.ai/ws"


# ---------------------------------------------------------------------------
# Event parsing
# ---------------------------------------------------------------------------


class TestEventParsing:
    def test_parse_session_ready(self) -> None:
        raw: dict[str, Any] = {"type": "session_ready", "session_id": "abc-123"}
        event = _parse_event(raw)
        assert isinstance(event, SessionReadyEvent)
        assert event.type == "session_ready"
        assert event.session_id == "abc-123"

    def test_parse_transcript(self) -> None:
        raw: dict[str, Any] = {"type": "transcript", "text": "Hello world", "is_final": True}
        event = _parse_event(raw)
        assert isinstance(event, TranscriptEvent)
        assert event.text == "Hello world"
        assert event.is_final is True

    def test_parse_context_update(self) -> None:
        raw: dict[str, Any] = {
            "type": "context_update",
            "context_version": 3,
            "ops": [
                {
                    "op": "add",
                    "card": {
                        "type": "episodic",
                        "claim": "User visited Paris last summer",
                        "score": 0.92,
                    },
                },
                {
                    "op": "add",
                    "card": {
                        "type": "preference",
                        "claim": "User prefers dark mode",
                        "score": 0.87,
                    },
                },
            ],
            "messages": [{"role": "system", "content": "context here"}],
        }
        event = _parse_event(raw)
        assert isinstance(event, ContextUpdateEvent)
        assert event.context_version == 3
        assert event.ops is not None
        assert len(event.ops) == 2
        assert event.ops[0].op == "add"
        assert event.ops[0].card is not None
        assert event.ops[0].card.type == "episodic"
        assert event.ops[0].card.claim == "User visited Paris last summer"
        assert event.messages is not None
        assert len(event.messages) == 1

    def test_parse_context_snapshot_as_context_update(self) -> None:
        raw: dict[str, Any] = {
            "type": "CONTEXT_SNAPSHOT",
            "context_version": 5,
            "ops": [{"op": "add", "card": {"type": "episodic", "claim": "Snapshot card"}}],
            "messages": [],
        }
        event = _parse_event(raw)
        assert isinstance(event, ContextUpdateEvent)
        assert event.type == "context_update"
        assert event.ops is not None
        assert len(event.ops) == 1
        assert event.ops[0].card is not None
        assert event.ops[0].card.claim == "Snapshot card"

    def test_parse_uppercase_event_types(self) -> None:
        raw: dict[str, Any] = {"type": "TRANSCRIPT", "text": "Hello", "is_final": True}
        event = _parse_event(raw)
        assert isinstance(event, TranscriptEvent)
        assert event.text == "Hello"

    def test_parse_session_ended(self) -> None:
        raw: dict[str, Any] = {"type": "session_ended", "reason": "timeout"}
        event = _parse_event(raw)
        assert isinstance(event, SessionEndedEvent)
        assert event.reason == "timeout"

    def test_parse_error(self) -> None:
        raw: dict[str, Any] = {"type": "error", "detail": "auth failed", "code": "AUTH_ERR"}
        event = _parse_event(raw)
        assert isinstance(event, ErrorEvent)
        assert event.detail == "auth failed"
        assert event.code == "AUTH_ERR"

    def test_parse_unknown_event_fallback(self) -> None:
        raw: dict[str, Any] = {"type": "some_future_event", "data": 123}
        event = _parse_event(raw)
        assert isinstance(event, SessionEndedEvent)


# ---------------------------------------------------------------------------
# ContextAccumulator
# ---------------------------------------------------------------------------


class TestContextAccumulator:
    def _make_context_update(
        self,
        cards: list[dict[str, Any]],
        *,
        version: int = 1,
        messages: list[dict[str, Any]] | None = None,
    ) -> ContextUpdateEvent:
        ops = [{"op": "add", "card": c} for c in cards]
        return ContextUpdateEvent.model_validate(
            {
                "type": "context_update",
                "context_version": version,
                "ops": ops,
                "messages": messages or [],
            }
        )

    def test_empty_accumulator(self) -> None:
        acc = ContextAccumulator()
        assert acc.build_context_string() == "(no context retrieved)"
        assert len(acc.cards) == 0
        assert len(acc.transcripts) == 0
        assert len(acc.messages) == 0

    def test_accumulate_context_cards(self) -> None:
        acc = ContextAccumulator()
        event = self._make_context_update(
            [
                {"type": "episodic", "claim": "User likes cats"},
                {"type": "preference", "claim": "Prefers Python"},
            ],
            version=1,
        )
        acc.on_context_update(event)

        assert len(acc.cards) == 2
        assert acc.cards[0].type == "episodic"
        assert acc.cards[0].claim == "User likes cats"
        assert acc.cards[1].type == "preference"
        assert acc.cards[1].claim == "Prefers Python"

    def test_accumulate_transcripts(self) -> None:
        acc = ContextAccumulator()
        acc.on_transcript(TranscriptEvent.model_validate({"type": "transcript", "text": "Hello"}))
        acc.on_transcript(TranscriptEvent.model_validate({"type": "transcript", "text": "World"}))
        acc.on_transcript(TranscriptEvent.model_validate({"type": "transcript", "text": "   "}))

        assert len(acc.transcripts) == 2
        assert acc.transcripts == ["Hello", "World"]

    def test_build_context_string_episodic(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update([{"type": "episodic", "claim": "Met at coffee shop"}])
        )
        result = acc.build_context_string()
        assert "Episodic Memories:" in result
        assert "Met at coffee shop" in result

    def test_build_context_string_preferences(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update([{"type": "preference", "claim": "Likes dark mode"}])
        )
        result = acc.build_context_string()
        assert "User Preferences:" in result
        assert "Likes dark mode" in result

    def test_build_context_string_identity(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update([{"type": "identity", "claim": "Name is Alice"}])
        )
        result = acc.build_context_string()
        assert "Identity Facts:" in result
        assert "Name is Alice" in result

    def test_build_context_string_visual(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update([{"type": "face_identity", "claim": "Recognized Bob"}])
        )
        result = acc.build_context_string()
        assert "Visual Observations:" in result
        assert "[face_identity] Recognized Bob" in result

    def test_build_context_string_with_transcript(self) -> None:
        acc = ContextAccumulator()
        acc.on_transcript(TranscriptEvent.model_validate({"type": "transcript", "text": "What is my name?"}))
        result = acc.build_context_string()
        assert "Transcript:" in result
        assert "What is my name?" in result

    def test_build_context_string_mixed(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update([
                {"type": "episodic", "claim": "Visited Paris"},
                {"type": "preference", "claim": "Likes jazz"},
                {"type": "identity", "claim": "Name is Eve"},
                {"type": "speaker_identity", "claim": "Speaker is Eve"},
            ])
        )
        acc.on_transcript(TranscriptEvent.model_validate({"type": "transcript", "text": "Remember me?"}))

        result = acc.build_context_string()
        assert "Episodic Memories:" in result
        assert "User Preferences:" in result
        assert "Identity Facts:" in result
        assert "Visual Observations:" in result
        assert "Transcript:" in result

    def test_build_llm_messages(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update([{"type": "episodic", "claim": "User loves pizza"}])
        )
        messages = acc.build_llm_messages("What food do I like?")
        assert len(messages) == 2
        assert messages[0]["role"] == "system"
        assert "User loves pizza" in messages[0]["content"]
        assert messages[1]["role"] == "user"
        assert messages[1]["content"] == "What food do I like?"

    def test_build_llm_messages_default_question(self) -> None:
        acc = ContextAccumulator()
        messages = acc.build_llm_messages()
        assert messages[1]["content"] == "Respond based on the context above."

    def test_context_version_tracking(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(self._make_context_update([], version=5))
        acc.on_context_update(self._make_context_update([], version=3))
        acc.on_context_update(self._make_context_update([], version=8))
        assert acc._context_version == 8

    def test_accumulate_messages(self) -> None:
        acc = ContextAccumulator()
        acc.on_context_update(
            self._make_context_update(
                [],
                messages=[
                    {"role": "system", "content": "msg1"},
                    {"role": "system", "content": "msg2"},
                ],
            )
        )
        assert len(acc.messages) == 2


# ---------------------------------------------------------------------------
# AsyncRealtimeSession — unit tests with mocked WebSocket
# ---------------------------------------------------------------------------


def _make_mock_ws(messages: list[str | bytes]) -> AsyncMock:
    """Create a mock WebSocket that yields the given messages then closes."""
    ws = AsyncMock()
    ws.send = AsyncMock()
    ws.close = AsyncMock()

    recv_iter = iter(messages)

    async def mock_recv() -> str | bytes:
        try:
            return next(recv_iter)
        except StopIteration:
            raise ConnectionError("connection closed")

    ws.recv = mock_recv
    return ws


class TestAsyncRealtimeSession:
    async def test_handshake_success(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "srv-session-1"})
        mock_ws = _make_mock_ws([ready_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="my-session",
                generation=False,
            )
            await session._connect()

            assert session.session_id == "srv-session-1"

            sent_data = mock_ws.send.call_args[0][0]
            init = json.loads(sent_data)
            assert init["token"] == "upl_test"
            assert init["session_id"] == "my-session"
            assert init["user_id"] == "user-1"
            assert init["generation"] is False

            await session.close()

    async def test_handshake_error(self) -> None:
        error_msg = json.dumps({"type": "error", "detail": "invalid token"})
        mock_ws = _make_mock_ws([error_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="bad_key",
                user_id="user-1",
                session_id="my-session",
            )
            with pytest.raises(Exception, match="Gateway handshake error"):
                await session._connect()

    async def test_send_audio(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        mock_ws = _make_mock_ws([ready_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
            )
            await session._connect()

            pcm = b"\x00\x01" * 160
            await session.send_audio(pcm)

            sent = mock_ws.send.call_args_list[-1][0][0]
            assert isinstance(sent, bytes)
            assert sent[0] == FRAME_AUDIO
            assert sent[1:] == pcm

            await session.close()

    async def test_send_video(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        mock_ws = _make_mock_ws([ready_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
            )
            await session._connect()

            jpeg = b"\xff\xd8\xff\xe0" + b"\x00" * 100
            await session.send_video(jpeg)

            sent = mock_ws.send.call_args_list[-1][0][0]
            assert isinstance(sent, bytes)
            assert sent[0] == FRAME_VIDEO
            assert sent[1:] == jpeg

            await session.close()

    async def test_recv_context_update(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        ctx_msg = json.dumps({
            "type": "context_update",
            "context_version": 1,
            "ops": [{"op": "add", "card": {"type": "episodic", "claim": "Likes hiking"}}],
            "messages": [],
        })
        mock_ws = _make_mock_ws([ready_msg, ctx_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
                generation=False,
            )
            await session._connect()

            event = await session.recv()
            assert isinstance(event, ContextUpdateEvent)
            assert len(session.context.cards) == 1
            assert session.context.cards[0].claim == "Likes hiking"

            await session.close()

    async def test_recv_transcript_auto_accumulates(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        transcript_msg = json.dumps({"type": "transcript", "text": "How are you?"})
        mock_ws = _make_mock_ws([ready_msg, transcript_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
            )
            await session._connect()

            event = await session.recv()
            assert isinstance(event, TranscriptEvent)
            assert event.text == "How are you?"
            assert "How are you?" in session.context.transcripts

            await session.close()

    async def test_recv_binary_returns_none(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        mock_ws = _make_mock_ws([ready_msg, b"\x00\x01\x02\x03"])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
            )
            await session._connect()

            event = await session.recv()
            assert event is None

            await session.close()

    async def test_async_iteration(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        messages = [
            ready_msg,
            json.dumps({"type": "transcript", "text": "Hi"}),
            json.dumps({
                "type": "context_update",
                "context_version": 1,
                "ops": [{"op": "add", "card": {"type": "episodic", "claim": "Test"}}],
            }),
            json.dumps({"type": "session_ended", "reason": "done"}),
        ]
        mock_ws = _make_mock_ws(messages)

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
                generation=False,
            )
            await session._connect()

            events: list[Any] = []
            async for event in session:
                events.append(event)

            assert len(events) == 3
            assert isinstance(events[0], TranscriptEvent)
            assert isinstance(events[1], ContextUpdateEvent)
            assert isinstance(events[2], SessionEndedEvent)

            assert len(session.context.transcripts) == 1
            assert len(session.context.cards) == 1

            await session.close()

    async def test_context_manager(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        mock_ws = _make_mock_ws([ready_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
            )
            async with session as s:
                assert s.session_id == "s1"
                assert s is session

            mock_ws.close.assert_called_once()

    async def test_handshake_includes_optional_fields(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        mock_ws = _make_mock_ws([ready_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
                generation=False,
                project_id="proj_ABC",
                persona_id="persona_XYZ",
                disabled_learning=True,
            )
            await session._connect()

            sent_data = mock_ws.send.call_args[0][0]
            init = json.loads(sent_data)
            assert init["project_id"] == "proj_ABC"
            assert init["persona_id"] == "persona_XYZ"
            assert init["disabled_learning"] is True
            assert init["generation"] is False

            await session.close()

    async def test_send_audio_when_closed_raises(self) -> None:
        session = AsyncRealtimeSession(
            api_key="upl_test",
            user_id="user-1",
            session_id="s1",
        )
        session._closed = True
        with pytest.raises(Exception, match="not connected"):
            await session.send_audio(b"\x00" * 320)

    async def test_send_video_when_closed_raises(self) -> None:
        session = AsyncRealtimeSession(
            api_key="upl_test",
            user_id="user-1",
            session_id="s1",
        )
        session._closed = True
        with pytest.raises(Exception, match="not connected"):
            await session.send_video(b"\xff\xd8" * 10)

    async def test_double_close_is_safe(self) -> None:
        ready_msg = json.dumps({"type": "session_ready", "session_id": "s1"})
        mock_ws = _make_mock_ws([ready_msg])

        with patch("elicitlabs.resources.realtime.session.websockets") as mock_websockets:
            mock_websockets.connect = AsyncMock(return_value=mock_ws)

            session = AsyncRealtimeSession(
                api_key="upl_test",
                user_id="user-1",
                session_id="s1",
            )
            await session._connect()
            await session.close()
            await session.close()

            mock_ws.close.assert_called_once()
