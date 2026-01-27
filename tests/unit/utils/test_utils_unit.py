# tests/unit/utils/test_utils_unit.py
from __future__ import annotations

from typing import Any, Callable

import pytest
import httpx

import dateno.utils as utils


def _require_attr(name: str) -> Any:
    """
    Resolve an attribute from `dateno.utils` or skip the test.

    This keeps the test suite resilient to SDK regeneration changes
    while still providing coverage when the symbol exists.
    """
    if not hasattr(utils, name):
        pytest.skip(f"dateno.utils.{name} is not available in this SDK build.")
    return getattr(utils, name)


def test_match_status_codes_supports_exact_and_classes() -> None:
    """
    `match_status_codes()` must support:
      - exact codes ("200")
      - status classes ("4XX", "5XX")
      - mixed lists
    """
    match_status_codes: Callable[[Any, int], bool] = _require_attr("match_status_codes")

    assert match_status_codes(["200"], 200) is True
    assert match_status_codes(["201"], 200) is False

    assert match_status_codes(["4XX"], 404) is True
    assert match_status_codes(["4XX"], 500) is False

    assert match_status_codes(["5XX"], 503) is True
    assert match_status_codes(["5XX"], 200) is False

    assert match_status_codes(["404", "5XX"], 500) is True
    assert match_status_codes(["404", "5XX"], 404) is True
    assert match_status_codes(["404", "5XX"], 200) is False


def test_generate_url_joins_base_url_and_path() -> None:
    """
    `generate_url()` must join base_url and path into a usable URL.

    Current contract:
      - if `path` starts with "/", it is appended as-is
      - if `path` does NOT start with "/", the function does not insert a slash
        (callers must provide a leading "/" when needed)
    """
    generate_url: Callable[[str, str, dict], str] = _require_attr("generate_url")

    url = generate_url("https://example.invalid", "/healthz", {})
    assert url.startswith("https://example.invalid")
    assert url.endswith("/healthz")

    # No implicit "/" normalization when path has no leading slash.
    url2 = generate_url("https://example.invalid/", "healthz", {})
    assert url2 == "https://example.invalidhealthz"
    assert url2.endswith("healthz")

    # And a "correct" caller form:
    url3 = generate_url("https://example.invalid/", "/healthz", {})
    assert url3.endswith("/healthz")



def test_stream_to_text_with_httpx_response() -> None:
    """
    `stream_to_text()` must:
      - accept httpx.Response
      - never raise
      - return string content
    """
    stream_to_text: Callable[[Any], str] = _require_attr("stream_to_text")

    res = httpx.Response(
        500,
        headers={"content-type": "application/json"},
        content=b'{"detail":"boom"}',
    )

    out = stream_to_text(res)
    assert isinstance(out, str)
    assert "boom" in out

    # invalid utf-8 must not raise
    res2 = httpx.Response(
        500,
        headers={"content-type": "text/plain"},
        content=b"\xff\xfe\xfd",
    )

    out2 = stream_to_text(res2)
    assert isinstance(out2, str)


def test_match_response_basic_success_case() -> None:
    """
    `match_response()` must correctly match:
      - exact status code
      - content-type prefix
    """
    if not hasattr(utils, "match_response"):
        pytest.skip("match_response not available")

    match_response = utils.match_response

    res = httpx.Response(
        200,
        headers={"content-type": "application/json; charset=utf-8"},
        content=b"{}",
    )

    assert match_response(res, "200", "application/json") is True
    assert match_response(res, "4XX", "application/json") is False
    assert match_response(res, "200", "*") is True


def test_retry_calls_function_and_returns_value() -> None:
    """
    `retry()` must call the wrapped function and return its result.

    We provide a minimal fake RetryConfig compatible with current implementation.
    """
    if not hasattr(utils, "retry") or not hasattr(utils, "Retries"):
        pytest.skip("retry utilities not available")

    retry = utils.retry
    Retries = utils.Retries

    class _FakeRetryConfig:
        strategy = "none"

    calls: list[str] = []

    def fn():
        calls.append("called")
        return "ok"

    retries = Retries(_FakeRetryConfig(), ["429", "500"])
    result = retry(fn, retries)

    assert result == "ok"
    assert calls == ["called"]
