"""Tests for the message-level file resolution logic in DataResource.ingest().

These tests verify that when content_type='messages' and the payload contains
multimodal content parts (image, audio, video, image_url), local file paths,
URLs, data URIs, and raw base64 values are uploaded to GCS via signed URLs
and replaced with the returned object key — while GCS keys and text parts
are left untouched.
"""

from __future__ import annotations

import base64
import tempfile
from pathlib import Path
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from elicitlabs.resources.data.data import (
    DataResource,
    AsyncDataResource,
    _is_already_gcs_key,
    _resolve_media_bytes,
    _MEDIA_PART_TYPES,
)


# ---------------------------------------------------------------------------
# Module-level helper tests
# ---------------------------------------------------------------------------

class TestIsAlreadyGcsKey:
    def test_typical_gcs_key(self):
        assert _is_already_gcs_key(
            "prod/org-abc/user-xyz/ingest/2026/03/27/file.png"
        ) is True

    def test_short_relative_path_is_not_gcs_key(self):
        assert _is_already_gcs_key("images/photo.png") is False

    def test_http_url_is_not_gcs_key(self):
        assert _is_already_gcs_key("https://example.com/image.png") is False

    def test_data_uri_is_not_gcs_key(self):
        assert _is_already_gcs_key("data:image/png;base64,abc") is False

    def test_empty_string(self):
        assert _is_already_gcs_key("") is False

    def test_absolute_unix_path_is_not_gcs_key(self):
        assert _is_already_gcs_key("/var/folders/m5/abc/file.png") is False

    def test_home_relative_path_is_not_gcs_key(self):
        assert _is_already_gcs_key("~/Documents/project/data/file.png") is False

    def test_dot_relative_path_is_not_gcs_key(self):
        assert _is_already_gcs_key("./assets/images/logo/icon.png") is False


class TestResolveMediaBytes:
    def test_data_uri_png(self):
        raw = b"\x89PNG_fake_image"
        encoded = base64.b64encode(raw).decode()
        data_uri = f"data:image/png;base64,{encoded}"
        result = _resolve_media_bytes(data_uri)
        assert result is not None
        file_bytes, ext = result
        assert file_bytes == raw
        assert ext == "png"

    def test_data_uri_jpeg(self):
        raw = b"\xff\xd8\xff_fake_jpeg"
        encoded = base64.b64encode(raw).decode()
        data_uri = f"data:image/jpeg;base64,{encoded}"
        result = _resolve_media_bytes(data_uri)
        assert result is not None
        file_bytes, ext = result
        assert file_bytes == raw
        assert ext == "jpeg"

    def test_raw_base64(self):
        raw = b"hello world bytes"
        encoded = base64.b64encode(raw).decode()
        result = _resolve_media_bytes(encoded)
        assert result is not None
        file_bytes, ext = result
        assert file_bytes == raw
        assert ext == "bin"

    def test_plain_text_returns_none(self):
        assert _resolve_media_bytes("just some plain text!") is None

    def test_invalid_data_uri_returns_none(self):
        assert _resolve_media_bytes("data:no_comma_here") is None

    def test_empty_string_returns_none(self):
        assert _resolve_media_bytes("") is None


# ---------------------------------------------------------------------------
# Helpers to build a mock DataResource without a real HTTP client
# ---------------------------------------------------------------------------

def _make_mock_resource() -> DataResource:
    """Build a DataResource with a mocked _upload_to_gcs."""
    resource = object.__new__(DataResource)
    resource._upload_to_gcs = MagicMock(  # type: ignore[method-assign]
        side_effect=lambda *, file_bytes, filename, user_id, project_id, persona_id: (
            f"prod/user-{user_id}/ingest/2026/03/{filename}"
        ),
    )
    return resource


# ---------------------------------------------------------------------------
# _resolve_message_files — sync
# ---------------------------------------------------------------------------

class TestResolveMessageFilesSync:
    """Verify _resolve_message_files on the sync DataResource."""

    def test_text_only_messages_unchanged(self):
        resource = _make_mock_resource()
        payload = [
            {"role": "user", "content": "Hello, just text"},
            {"role": "user", "content": [{"type": "text", "text": "More text"}]},
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result == payload
        resource._upload_to_gcs.assert_not_called()

    def test_gcs_key_left_untouched(self):
        resource = _make_mock_resource()
        gcs_key = "prod/org-abc/user-xyz/ingest/2026/03/27/photo.png"
        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "content": gcs_key},
                ],
            }
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result[0]["content"][0]["content"] == gcs_key
        resource._upload_to_gcs.assert_not_called()

    def test_local_file_path_uploaded_and_replaced(self):
        resource = _make_mock_resource()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG_fake")
            tmp_path = f.name

        try:
            payload = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Look at this:"},
                        {"type": "image", "content": tmp_path},
                    ],
                }
            ]
            result = resource._resolve_message_files(
                payload=payload, user_id="u1",
            )
            img_part = result[0]["content"][1]
            assert img_part["content"].startswith("prod/")
            assert img_part["content"].endswith(".png")
            resource._upload_to_gcs.assert_called_once()

            # Original payload must NOT be mutated
            assert payload[0]["content"][1]["content"] == tmp_path
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_data_uri_uploaded_and_replaced(self):
        resource = _make_mock_resource()
        raw = b"\x89PNG_fake_image_data"
        encoded = base64.b64encode(raw).decode()
        data_uri = f"data:image/png;base64,{encoded}"

        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "content": data_uri},
                ],
            }
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result[0]["content"][0]["content"].startswith("prod/")
        call_kwargs = resource._upload_to_gcs.call_args
        assert call_kwargs.kwargs["file_bytes"] == raw
        assert call_kwargs.kwargs["filename"] == "inline_media.png"

    def test_raw_base64_uploaded_and_replaced(self):
        resource = _make_mock_resource()
        raw = b"raw_image_bytes_here"
        encoded = base64.b64encode(raw).decode()

        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "audio", "content": encoded},
                ],
            }
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result[0]["content"][0]["content"].startswith("prod/")
        call_kwargs = resource._upload_to_gcs.call_args
        assert call_kwargs.kwargs["file_bytes"] == raw

    def test_image_url_type_resolved(self):
        """image_url parts should have image_url.url replaced."""
        resource = _make_mock_resource()
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            f.write(b"\xff\xd8\xff_fake")
            tmp_path = f.name

        try:
            payload = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": tmp_path}},
                    ],
                }
            ]
            result = resource._resolve_message_files(
                payload=payload, user_id="u1",
            )
            url_val = result[0]["content"][0]["image_url"]["url"]
            assert url_val.startswith("prod/")
            assert url_val.endswith(".jpg")
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_image_url_gcs_key_left_untouched(self):
        resource = _make_mock_resource()
        gcs_key = "prod/org-abc/user-xyz/ingest/2026/03/27/photo.jpg"
        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": gcs_key}},
                ],
            }
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result[0]["content"][0]["image_url"]["url"] == gcs_key
        resource._upload_to_gcs.assert_not_called()

    def test_http_url_downloaded_and_uploaded(self):
        resource = _make_mock_resource()
        fake_bytes = b"downloaded_image_content"

        with patch(
            "elicitlabs.resources.data.data._download_from_url",
            return_value=(fake_bytes, "remote_image.png"),
        ) as mock_dl:
            payload = [
                {
                    "role": "user",
                    "content": [
                        {"type": "video", "content": "https://example.com/video.mp4"},
                    ],
                }
            ]
            result = resource._resolve_message_files(
                payload=payload, user_id="u1",
            )
            mock_dl.assert_called_once_with("https://example.com/video.mp4")
            assert result[0]["content"][0]["content"].startswith("prod/")

    def test_multiple_parts_mixed(self):
        """Multiple parts in one message: text stays, GCS key stays, file uploaded."""
        resource = _make_mock_resource()
        gcs_key = "prod/org/user/ingest/2026/03/existing.png"
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(b"RIFF_fake_audio")
            audio_path = f.name

        try:
            payload = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Description"},
                        {"type": "image", "content": gcs_key},
                        {"type": "audio", "content": audio_path},
                    ],
                }
            ]
            result = resource._resolve_message_files(
                payload=payload, user_id="u1",
            )
            parts = result[0]["content"]
            assert parts[0] == {"type": "text", "text": "Description"}
            assert parts[1]["content"] == gcs_key
            assert parts[2]["content"].startswith("prod/")
            assert parts[2]["content"].endswith(".wav")
            resource._upload_to_gcs.assert_called_once()
        finally:
            Path(audio_path).unlink(missing_ok=True)

    def test_non_media_types_ignored(self):
        """Content parts with types outside MEDIA_PART_TYPES are skipped."""
        resource = _make_mock_resource()
        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "hello"},
                    {"type": "custom_widget", "content": "/tmp/something"},
                ],
            }
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result == payload
        resource._upload_to_gcs.assert_not_called()

    def test_empty_content_value_skipped(self):
        resource = _make_mock_resource()
        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "content": ""},
                ],
            }
        ]
        result = resource._resolve_message_files(
            payload=payload, user_id="u1",
        )
        assert result[0]["content"][0]["content"] == ""
        resource._upload_to_gcs.assert_not_called()

    def test_multiple_messages(self):
        resource = _make_mock_resource()
        raw = b"some_bytes"
        encoded = base64.b64encode(raw).decode()
        data_uri = f"data:audio/mp3;base64,{encoded}"

        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG")
            img_path = f.name

        try:
            payload = [
                {
                    "role": "system",
                    "content": "You are helpful.",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "content": img_path},
                    ],
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "audio", "content": data_uri},
                    ],
                },
            ]
            result = resource._resolve_message_files(
                payload=payload, user_id="u1",
            )
            # system message (plain string content) unchanged
            assert result[0]["content"] == "You are helpful."
            # image resolved
            assert result[1]["content"][0]["content"].startswith("prod/")
            # audio resolved
            assert result[2]["content"][0]["content"].startswith("prod/")
            assert resource._upload_to_gcs.call_count == 2
        finally:
            Path(img_path).unlink(missing_ok=True)

    def test_pathlib_path_object(self):
        resource = _make_mock_resource()
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
            f.write(b"\x89PNG_pathlib")
            tmp_path = Path(f.name)

        try:
            payload = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "content": tmp_path},
                    ],
                }
            ]
            result = resource._resolve_message_files(
                payload=payload, user_id="u1",
            )
            assert result[0]["content"][0]["content"].startswith("prod/")
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_missing_file_raises(self):
        resource = _make_mock_resource()
        payload = [
            {
                "role": "user",
                "content": [
                    {"type": "image", "content": Path("/nonexistent/fake.png")},
                ],
            }
        ]
        with pytest.raises(FileNotFoundError):
            resource._resolve_message_files(payload=payload, user_id="u1")


# ---------------------------------------------------------------------------
# Verify that _MEDIA_PART_TYPES has the expected members
# ---------------------------------------------------------------------------

class TestMediaPartTypes:
    def test_expected_types(self):
        assert _MEDIA_PART_TYPES == {"image", "audio", "video"}

    def test_text_not_in_media(self):
        assert "text" not in _MEDIA_PART_TYPES
