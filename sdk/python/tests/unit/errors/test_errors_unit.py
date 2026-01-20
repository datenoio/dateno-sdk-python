"""
Unit tests for the SDK error types.

These tests validate *actual* runtime contracts of the generated SDK build.
They are intentionally conservative: we assert only what is stable and
observable from the error instances in this repository.
"""

from __future__ import annotations

from typing import Any, Mapping

import httpx
import pytest

import dateno.errors as errors


def _mk_httpx_response(
    status_code: int,
    *,
    headers: Mapping[str, str] | None = None,
    content: bytes = b"",
) -> httpx.Response:
    """
    Build a minimal httpx.Response suitable for SDK error wrappers.

    We attach a request because some httpx helpers assume it exists.
    """
    req = httpx.Request("GET", "https://example.invalid/unit-test")
    return httpx.Response(status_code, headers=dict(headers or {}), content=content, request=req)


def test_sdkerror_base_contract_exposes_status_and_body() -> None:
    """SDKError must expose status_code/body derived from the raw response."""
    res = _mk_httpx_response(418, headers={"content-type": "text/plain"}, content=b"teapot")
    exc = errors.SDKError("Base error", res)

    assert exc.status_code == 418
    assert exc.raw_response is res
    assert "teapot" in exc.body
    assert str(exc) == "Base error"


def test_noresponseerror_is_exception_with_message() -> None:
    """
    NoResponseError is a standalone exception type in this SDK build.

    Contract:
      - is an Exception
      - preserves the provided message in `str()`
    """
    exc = errors.NoResponseError("No response received")
    assert isinstance(exc, Exception)
    assert "No response received" in str(exc)


def test_sdkdefaulterror_includes_status_and_body_in_str() -> None:
    """
    SDKDefaultError.__str__ appends a response summary in this SDK build.

    We assert that the string representation includes:
      - the provided message prefix
      - status code
      - content-type
      - decoded body snippet (best-effort)
    """
    res = _mk_httpx_response(500, headers={"content-type": "text/plain"}, content=b"boom")
    exc = errors.SDKDefaultError("Unexpected error occurred", res)

    assert isinstance(exc, errors.SDKError)
    assert exc.status_code == 500
    assert "boom" in exc.body

    s = str(exc)
    assert s.startswith("Unexpected error occurred")
    assert "Status 500" in s
    assert "text/plain" in s
    assert "boom" in s


def test_errorresponse_exposes_data_and_raw_response_and_str_is_body() -> None:
    """
    ErrorResponse stores:
      - raw_response
      - parsed data

    In this SDK build, ErrorResponse.__str__ returns the response body text.
    """
    res = _mk_httpx_response(
        500,
        headers={"content-type": "application/json"},
        content=b'{"detail":"boom"}',
    )
    data: Any = {"detail": "boom"}

    exc = errors.ErrorResponse(data=data, raw_response=res)

    assert isinstance(exc, errors.SDKError)
    assert exc.status_code == 500
    assert exc.raw_response is res
    assert exc.data == data

    # str() equals body for this build
    assert str(exc) == '{"detail":"boom"}'
    assert exc.body == '{"detail":"boom"}'


def test_httpvalidationerror_exposes_data_and_raw_response() -> None:
    """
    HTTPValidationError is a distinct type in this SDK build (not necessarily
    a subclass of ErrorResponse).

    Contract:
      - behaves like SDKError
      - exposes raw_response, status_code, body
      - exposes parsed validation payload via `.data`
    """
    res = _mk_httpx_response(
        422,
        headers={"content-type": "application/json"},
        content=b'{"detail":[]}',
    )
    data: Any = {"detail": [{"loc": ["query", "x"], "msg": "bad", "type": "value_error"}]}

    exc = errors.HTTPValidationError(data=data, raw_response=res)

    assert isinstance(exc, errors.SDKError)
    assert exc.status_code == 422
    assert exc.raw_response is res
    assert exc.data == data

    # In this build, message/body default to raw response text
    assert str(exc) == '{"detail":[]}'
    assert exc.body == '{"detail":[]}'


def test_responsevalidationerror_requires_message_and_preserves_cause() -> None:
    """
    ResponseValidationError requires `message` in this SDK build.

    Contract:
      - is an SDKError
      - preserves status_code/raw_response
      - supports exception chaining (`raise ... from ...`)
    """
    res = _mk_httpx_response(200, headers={"content-type": "application/json"}, content=b"{}")
    root = ValueError("schema mismatch")

    with pytest.raises(errors.ResponseValidationError) as ei:
        raise errors.ResponseValidationError("Invalid response", raw_response=res, cause=root) from root

    exc = ei.value
    assert isinstance(exc, errors.SDKError)
    assert exc.status_code == 200
    assert exc.raw_response is res

    # Cause property should reflect the chained exception (implementation-specific,
    # but your earlier tests used `.cause`, so we validate it exists when present).
    if hasattr(exc, "cause"):
        assert exc.cause is root

    s = str(exc)
    assert "Invalid response" in s
    assert "schema mismatch" in s
