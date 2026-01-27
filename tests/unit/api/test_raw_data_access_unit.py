# tests/test_raw_data_access_unit.py
"""
Unit tests for the `RawDataAccess` client (sync only).

Scope:
    These tests validate SDK *client-side* logic for the Raw Data Access API:
      - request construction for synchronous methods
      - response-branch selection based on HTTP status and Content-Type
      - correct model type passed into `unmarshal_json_response`
      - correct exception type raised for error responses

Non-goals:
    - transport behavior of httpx (covered by integration tests)
    - correctness of `dateno.utils.match_response` (patched with deterministic fake)
    - server-side API correctness

Why these tests matter:
    The SDK is generated code; regressions most often occur in:
      - path templates (e.g. "/raw/0.1/entry/{entry_id}")
      - operation_id wiring in HookContext
      - status-code branching and exception selection

Dependencies:
    We reuse deterministic helpers from `tests.test_utils` to avoid duplicating
    fake response types and matcher logic across test files.
"""

from __future__ import annotations

from typing import Any

import pytest

import dateno.raw_data_access as raw_mod
from dateno import errors
from dateno.raw_data_access import RawDataAccess
from test_utils import (
    FakeResponse,
    assert_request_common,
    make_unmarshal_json_response_stub,
    mk_cfg,
    patch_match_response,
)


def test_get_raw_entry_by_id_builds_request_and_returns_unmarshaled(monkeypatch) -> None:
    """
    Ensure `get_raw_entry_by_id()`:
      - builds the expected request (method/path/base_url)
      - matches the 200 JSON branch
      - requests `SearchIndexEntry` from `unmarshal_json_response`
      - returns the unmarshaled value

    This test is intentionally strict about the path template and request type,
    because those are the most common breaking points after SDK regeneration.
    """
    api = RawDataAccess(mk_cfg())

    captured: dict[str, Any] = {}

    def fake_build_request(*, method, path, base_url, request, **kwargs):
        captured["build"] = {
            "method": method,
            "path": path,
            "base_url": base_url,
            "request_type": type(request).__name__,
        }
        return object()

    def fake_do_request(*, hook_ctx, request, **kwargs):
        captured["do"] = {"operation_id": getattr(hook_ctx, "operation_id", None)}
        return FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b'{"ok": true}',
        )

    monkeypatch.setattr(api, "_build_request", fake_build_request)
    monkeypatch.setattr(api, "do_request", fake_do_request)

    patch_match_response(monkeypatch)

    unmarshal_stub = make_unmarshal_json_response_stub(
        {
            "SearchIndexEntry": {"unmarshaled": True},
        }
    )
    monkeypatch.setattr(raw_mod, "unmarshal_json_response", unmarshal_stub)

    result = api.get_raw_entry_by_id(entry_id="abc123", apikey="k")

    assert result == {"unmarshaled": True}
    assert_request_common(
        captured["build"],
        method="GET",
        path="/raw/0.1/entry/{entry_id}",
        base_url="https://example.invalid",
        request_type="GetRawEntryByIDRequest",
    )
    assert captured["do"]["operation_id"] == "get_raw_entry_by_id"


def test_get_raw_entry_by_id_500_raises_error_response(monkeypatch) -> None:
    """
    Ensure `get_raw_entry_by_id()` raises `errors.ErrorResponse` for server errors.

    Validates the 500 error branch:
      - response is matched as a 5XX
      - body is unmarshaled into `errors.ErrorResponseData`
      - SDK raises `errors.ErrorResponse`

    We intentionally do not assert the full payload structure here; the critical
    contract is the exception class and the fact that the error path is taken.
    """
    api = RawDataAccess(mk_cfg())

    monkeypatch.setattr(api, "_build_request", lambda **kwargs: object())
    monkeypatch.setattr(
        api,
        "do_request",
        lambda **kwargs: FakeResponse(
            500,
            headers={"Content-Type": "application/json"},
            content=b'{"detail":"boom"}',
        ),
    )

    patch_match_response(monkeypatch)

    unmarshal_stub = make_unmarshal_json_response_stub(
        {
            errors.ErrorResponseData: {"detail": "boom"},
        }
    )
    monkeypatch.setattr(raw_mod, "unmarshal_json_response", unmarshal_stub)

    with pytest.raises(errors.ErrorResponse):
        api.get_raw_entry_by_id(entry_id="abc123", apikey="k")
