# tests/unit/utils/test_utils_unit.py
from __future__ import annotations

from typing import Any, Callable, Type

import pytest
import httpx

import dateno.utils as utils
import dateno.utils.retries as retries_mod


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


def _make_retries(retry_connection_errors: bool) -> Any:
    BackoffStrategy = _require_attr("BackoffStrategy")
    RetryConfig = _require_attr("RetryConfig")
    Retries = _require_attr("Retries")

    backoff = BackoffStrategy(
        initial_interval=0,
        max_interval=0,
        exponent=1.0,
        max_elapsed_time=5000,
    )
    config = RetryConfig(
        strategy="backoff",
        backoff=backoff,
        retry_connection_errors=retry_connection_errors,
    )
    return Retries(config, ["500"])


def _patch_retry_sleep(monkeypatch) -> None:
    monkeypatch.setattr(retries_mod.random, "uniform", lambda *_: 0)
    monkeypatch.setattr(retries_mod.time, "sleep", lambda *_: None)


@pytest.mark.parametrize("exc_type", [httpx.ConnectError, httpx.ReadTimeout])
def test_retry_retries_connection_errors_when_enabled(
    monkeypatch, exc_type: Type[Exception]
) -> None:
    """
    `retry()` should retry connection errors when the flag is enabled.
    """
    if not hasattr(utils, "retry"):
        pytest.skip("retry utilities not available")

    retry = utils.retry
    retries = _make_retries(True)
    _patch_retry_sleep(monkeypatch)

    calls = {"count": 0}
    request = httpx.Request("GET", "https://example.invalid")

    def fn():
        calls["count"] += 1
        if calls["count"] == 1:
            raise exc_type("boom", request=request)
        return httpx.Response(200)

    res = retry(fn, retries)

    assert res.status_code == 200
    assert calls["count"] == 2


@pytest.mark.parametrize("exc_type", [httpx.ConnectError, httpx.ReadTimeout])
def test_retry_does_not_retry_connection_errors_when_disabled(
    monkeypatch, exc_type: Type[Exception]
) -> None:
    """
    `retry()` should not retry connection errors when the flag is disabled.
    """
    if not hasattr(utils, "retry"):
        pytest.skip("retry utilities not available")

    retry = utils.retry
    retries = _make_retries(False)
    _patch_retry_sleep(monkeypatch)

    calls = {"count": 0}
    request = httpx.Request("GET", "https://example.invalid")

    def fn():
        calls["count"] += 1
        raise exc_type("boom", request=request)

    with pytest.raises(exc_type):
        retry(fn, retries)

    assert calls["count"] == 1


@pytest.mark.anyio
@pytest.mark.parametrize("exc_type", [httpx.ConnectError, httpx.ReadTimeout])
async def test_retry_async_retries_connection_errors_when_enabled(
    monkeypatch, exc_type: Type[Exception]
) -> None:
    """
    `retry_async()` should retry connection errors when the flag is enabled.
    """
    if not hasattr(utils, "retry_async"):
        pytest.skip("retry utilities not available")

    async def _noop_sleep(_):
        return None

    monkeypatch.setattr(retries_mod.random, "uniform", lambda *_: 0)
    monkeypatch.setattr(retries_mod.asyncio, "sleep", _noop_sleep)

    retry_async = utils.retry_async
    retries = _make_retries(True)

    calls = {"count": 0}
    request = httpx.Request("GET", "https://example.invalid")

    async def fn():
        calls["count"] += 1
        if calls["count"] == 1:
            raise exc_type("boom", request=request)
        return httpx.Response(200)

    res = await retry_async(fn, retries)

    assert res.status_code == 200
    assert calls["count"] == 2


@pytest.mark.anyio
@pytest.mark.parametrize("exc_type", [httpx.ConnectError, httpx.ReadTimeout])
async def test_retry_async_does_not_retry_connection_errors_when_disabled(
    monkeypatch, exc_type: Type[Exception]
) -> None:
    """
    `retry_async()` should not retry connection errors when the flag is disabled.
    """
    if not hasattr(utils, "retry_async"):
        pytest.skip("retry utilities not available")

    async def _noop_sleep(_):
        return None

    monkeypatch.setattr(retries_mod.random, "uniform", lambda *_: 0)
    monkeypatch.setattr(retries_mod.asyncio, "sleep", _noop_sleep)

    retry_async = utils.retry_async
    retries = _make_retries(False)

    calls = {"count": 0}
    request = httpx.Request("GET", "https://example.invalid")

    async def fn():
        calls["count"] += 1
        raise exc_type("boom", request=request)

    with pytest.raises(exc_type):
        await retry_async(fn, retries)

    assert calls["count"] == 1
