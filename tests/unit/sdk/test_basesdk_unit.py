from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional

import httpx
import pytest

import dateno.basesdk as basesdk_mod
from dateno.basesdk import BaseSDK
from dateno import errors

from test_utils import mk_cfg, patch_match_response


def make_httpx_response(
    status_code: int,
    *,
    content_type: str = "application/json",
    body: bytes = b"{}",
    url: str = "https://example.invalid/resp",
) -> httpx.Response:
    """
    Create a minimal httpx.Response suitable for BaseSDK unit tests.

    BaseSDK logs `response.url`, `response.headers`, and `response.text`, so we
    attach an httpx.Request to avoid httpx internals failing on missing request.
    """
    req = httpx.Request("GET", url)
    return httpx.Response(
        status_code=status_code,
        headers={"Content-Type": content_type},
        content=body,
        request=req,
    )


class _FakeDebugLogger:
    """
    Minimal logger stub.

    BaseSDK calls `logger.debug(...)` in both success and error flows. In unit
    tests we don't validate logging output, but we must provide a compatible API.
    """

    def debug(self, *args: Any, **kwargs: Any) -> None:  # noqa: D401
        return


class _FakeHooks:
    """
    Minimal hooks implementation compatible with Speakeasy hook orchestration.

    BaseSDK expects the hooks object to expose:
      - before_request(ctx, request) -> httpx.Request
      - after_success(ctx, response) -> httpx.Response
      - after_error(ctx, response|None, err|None) -> tuple[httpx.Response|None, Exception|None]

    We also keep counters so tests can assert which callbacks were invoked.
    """

    def __init__(self, *, request_to_return: Optional[httpx.Request] = None) -> None:
        self.before_request_calls = 0
        self.after_success_calls = 0
        self.after_error_calls = 0
        self._request_to_return = request_to_return or httpx.Request(
            "GET", "https://example.invalid/request"
        )

    def before_request(self, ctx: Any, request: Any) -> httpx.Request:
        self.before_request_calls += 1
        return self._request_to_return

    def after_success(self, ctx: Any, response: httpx.Response) -> httpx.Response:
        self.after_success_calls += 1
        return response

    def after_error(
        self, ctx: Any, response: Optional[httpx.Response], err: Optional[Exception]
    ) -> tuple[Optional[httpx.Response], Optional[Exception]]:
        self.after_error_calls += 1
        # Preserve the original behavior: do not transform response, do not swallow errors.
        return None, err


@dataclass
class _FakeHookCtx:
    """
    HookContext stub required by dateno._hooks.types.*Context wrappers.

    The generated hook context wrappers access the following attributes:
      - config
      - base_url
      - operation_id
      - oauth2_scopes
      - security_source
    """

    config: Any
    base_url: str
    operation_id: str
    oauth2_scopes: list[str]
    security_source: Any = None


class _FakeSyncClient:
    """
    Fake sync httpx-like client for BaseSDK tests.

    Responsibilities:
      - build_request(...): capture arguments and return a real httpx.Request
      - send(request, stream=False): return a preconfigured httpx.Response
    """

    def __init__(self, response: httpx.Response) -> None:
        self._response = response
        self.build_calls: list[dict[str, Any]] = []
        self.send_calls: list[dict[str, Any]] = []

    def build_request(
        self,
        method: str,
        url: str,
        *,
        params: Any = None,
        content: Any = None,
        data: Any = None,
        files: Any = None,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Any = None,
    ) -> httpx.Request:
        self.build_calls.append(
            {
                "method": method,
                "url": url,
                "params": params,
                "content": content,
                "data": data,
                "files": files,
                "headers": dict(headers or {}),
                "timeout": timeout,
            }
        )
        return httpx.Request(method, url, params=params, headers=headers)

    def send(self, request: httpx.Request, *, stream: bool = False) -> httpx.Response:
        self.send_calls.append({"request": request, "stream": stream})
        return self._response


class _FakeAsyncClient:
    """
    Fake async httpx-like client for BaseSDK tests.

    Mirrors `_FakeSyncClient`, but `send()` is async.
    """

    def __init__(self, response: httpx.Response) -> None:
        self._response = response
        self.send_calls: list[dict[str, Any]] = []

    async def send(self, request: httpx.Request, *, stream: bool = False) -> httpx.Response:
        self.send_calls.append({"request": request, "stream": stream})
        return self._response


@pytest.fixture
def anyio_backend():
    """Force anyio to use asyncio so we don't require trio in the test deps."""
    return "asyncio"


def _install_hooks(cfg: Any, hooks: _FakeHooks) -> None:
    """
    Install hooks into SDKConfiguration the way Speakeasy code expects.

    BaseSDK reads hooks from:
        cfg.__dict__["_hooks"]
    """
    cfg.__dict__["_hooks"] = hooks


def test_build_request_with_client_applies_security_and_merges_query_params_and_headers(monkeypatch) -> None:
    """
    `_build_request_with_client()` must:
      - build URL via `utils.generate_url(...)` when `url_override` is not provided
      - get query params via `utils.get_query_params(...)`
      - merge security headers/query params from `utils.get_security(security)`
      - include Accept + User-Agent headers
      - overlay `http_headers` on top of computed headers
      - pass merged params/headers into `client.build_request(params=..., headers=...)`
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()
    sdk = BaseSDK(cfg)

    # Make URL generation deterministic and independent from template_url details.
    monkeypatch.setattr(sdk, "_get_url", lambda base_url, url_variables: str(base_url))
    monkeypatch.setattr(basesdk_mod.utils, "generate_url", lambda *args, **kwargs: "https://example.invalid/x")

    # Deterministic query/header extraction.
    monkeypatch.setattr(basesdk_mod.utils, "get_query_params", lambda *args, **kwargs: {"limit": 10})
    monkeypatch.setattr(basesdk_mod.utils, "get_headers", lambda *args, **kwargs: {"X-Base": "1"})

    # Security merge.
    def fake_get_security(_security: Any) -> tuple[dict[str, str], dict[str, Any]]:
        return {"Authorization": "Bearer TEST"}, {"api_key": "K"}

    monkeypatch.setattr(basesdk_mod.utils, "get_security", fake_get_security)

    client = _FakeSyncClient(make_httpx_response(200))
    req = sdk._build_request_with_client(
        client,
        "GET",
        "/registry/catalog/x",
        "https://example.invalid",
        None,   # url_variables
        object(),  # request (opaque for this test)
        False,  # request_body_required
        False,  # request_has_path_params
        True,   # request_has_query_params
        "User-Agent",
        "application/json",
        None,   # _globals
        {"type": "apiKey"},  # security
        1000,   # timeout_ms
        None,   # get_serialized_body
        None,   # url_override
        {"X-Test": "1"},  # http_headers (overlay)
        None,   # allow_empty_value
    )

    assert isinstance(req, httpx.Request)
    assert client.build_calls, "Expected client.build_request() to be called exactly once"

    call = client.build_calls[0]
    assert call["method"] == "GET"
    assert call["url"] == "https://example.invalid/x"

    # Query params must include both base query params and security query params.
    assert call["params"]["limit"] == 10
    assert call["params"]["api_key"] == "K"

    # Headers must include computed headers + security headers + overlay headers.
    assert call["headers"]["X-Base"] == "1"
    assert call["headers"]["Authorization"] == "Bearer TEST"
    assert call["headers"]["X-Test"] == "1"
    assert call["headers"]["Accept"] == "application/json"
    assert "User-Agent" in call["headers"]


def test_build_request_with_client_requires_body_when_request_body_required(monkeypatch) -> None:
    """
    If `request_body_required=True` and `get_serialized_body()` returns None,
    `_build_request_with_client()` must raise ValueError("request body is required").
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()
    sdk = BaseSDK(cfg)

    client = _FakeSyncClient(make_httpx_response(200))

    def get_serialized_body_none():
        return None

    with pytest.raises(ValueError, match="request body is required"):
        sdk._build_request_with_client(
            client,
            "POST",
            "/somewhere",
            "https://example.invalid",
            None,
            object(),
            True,   # request_body_required
            False,
            False,
            "User-Agent",
            "application/json",
            None,
            None,
            1000,
            get_serialized_body_none,
            None,
            None,
            None,
        )


def test_do_request_success_calls_hooks_and_returns_response(monkeypatch) -> None:
    """
    `do_request()` success path:

      - calls hooks.before_request(...)
      - calls client.send(...)
      - since status is NOT in `error_status_codes`, calls hooks.after_success(...)
      - returns the response unchanged
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()

    hooks = _FakeHooks()
    _install_hooks(cfg, hooks)

    response = make_httpx_response(200, body=b'{"ok":true}')
    cfg.client = _FakeSyncClient(response)

    sdk = BaseSDK(cfg)

    hook_ctx = _FakeHookCtx(
        config=cfg,
        base_url="https://example.invalid",
        operation_id="unit_test_op",
        oauth2_scopes=[],
        security_source=None,
    )

    res = sdk.do_request(
        hook_ctx=hook_ctx,
        request=object(),
        error_status_codes=["4XX", "5XX"],
        retry_config=None,
    )

    assert res.status_code == 200
    assert hooks.before_request_calls == 1
    assert hooks.after_error_calls == 0
    assert hooks.after_success_calls == 1


def test_do_request_error_calls_hooks_and_raises_sdk_default_error(monkeypatch) -> None:
    """
    `do_request()` error path:

      - calls hooks.before_request(...)
      - calls client.send(...)
      - if status matches `error_status_codes`, calls hooks.after_error(...)
      - raises errors.SDKDefaultError
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()

    hooks = _FakeHooks()
    _install_hooks(cfg, hooks)

    response = make_httpx_response(500, body=b'{"detail":"boom"}')
    cfg.client = _FakeSyncClient(response)

    sdk = BaseSDK(cfg)

    hook_ctx = _FakeHookCtx(
        config=cfg,
        base_url="https://example.invalid",
        operation_id="unit_test_op",
        oauth2_scopes=[],
        security_source=None,
    )

    with pytest.raises(errors.SDKDefaultError) as exc_info:
        sdk.do_request(
            hook_ctx=hook_ctx,
            request=object(),
            error_status_codes=["5XX"],
            retry_config=None,
        )

    assert "boom" in str(exc_info.value)
    assert hooks.before_request_calls == 1
    assert hooks.after_error_calls == 1
    assert hooks.after_success_calls == 0


def test_do_request_uses_retry_helper_when_configured(monkeypatch) -> None:
    """
    When `retry_config` is provided, BaseSDK must call `utils.retry(do, Retries(...))`.

    We don't validate retry semantics here; only delegation + that it returns
    the wrapped `do()` result.
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()

    hooks = _FakeHooks()
    _install_hooks(cfg, hooks)

    response = make_httpx_response(200)
    cfg.client = _FakeSyncClient(response)

    sdk = BaseSDK(cfg)

    captured: dict[str, Any] = {}

    def fake_retry(func: Any, retries: Any) -> Any:
        captured["func"] = func
        captured["retries"] = retries
        return func()

    monkeypatch.setattr(basesdk_mod.utils, "retry", fake_retry)

    hook_ctx = _FakeHookCtx(
        config=cfg,
        base_url="https://example.invalid",
        operation_id="unit_test_op",
        oauth2_scopes=[],
        security_source=None,
    )

    res = sdk.do_request(
        hook_ctx=hook_ctx,
        request=object(),
        error_status_codes=["5XX"],
        retry_config=(object(), ["429", "500"]),
    )

    assert res.status_code == 200
    assert "func" in captured and "retries" in captured
    assert hooks.after_success_calls == 1


@pytest.mark.anyio
async def test_do_request_async_success_calls_hooks_and_returns_response(monkeypatch) -> None:
    """
    `do_request_async()` mirrors `do_request()` for async clients on the success path.
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()

    hooks = _FakeHooks()
    _install_hooks(cfg, hooks)

    response = make_httpx_response(200)
    cfg.async_client = _FakeAsyncClient(response)

    sdk = BaseSDK(cfg)

    hook_ctx = _FakeHookCtx(
        config=cfg,
        base_url="https://example.invalid",
        operation_id="unit_test_op",
        oauth2_scopes=[],
        security_source=None,
    )

    res = await sdk.do_request_async(
        hook_ctx=hook_ctx,
        request=object(),
        error_status_codes=["4XX", "5XX"],
        retry_config=None,
    )

    assert res.status_code == 200
    assert hooks.before_request_calls == 1
    assert hooks.after_error_calls == 0
    assert hooks.after_success_calls == 1


@pytest.mark.anyio
async def test_do_request_async_error_calls_hooks_and_raises_sdk_default_error(monkeypatch) -> None:
    """
    `do_request_async()` must raise SDKDefaultError when status matches error codes.
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()

    hooks = _FakeHooks()
    _install_hooks(cfg, hooks)

    response = make_httpx_response(503, body=b'{"detail":"down"}')
    cfg.async_client = _FakeAsyncClient(response)

    sdk = BaseSDK(cfg)

    hook_ctx = _FakeHookCtx(
        config=cfg,
        base_url="https://example.invalid",
        operation_id="unit_test_op",
        oauth2_scopes=[],
        security_source=None,
    )

    with pytest.raises(errors.SDKDefaultError) as exc_info:
        await sdk.do_request_async(
            hook_ctx=hook_ctx,
            request=object(),
            error_status_codes=["503", "5XX"],
            retry_config=None,
        )

    assert "down" in str(exc_info.value)
    assert hooks.before_request_calls == 1
    assert hooks.after_error_calls == 1
    assert hooks.after_success_calls == 0


@pytest.mark.anyio
async def test_do_request_async_uses_retry_async_when_configured(monkeypatch) -> None:
    """
    When `retry_config` is provided, BaseSDK must call `utils.retry_async(do, Retries(...))`.
    """
    patch_match_response(monkeypatch)

    cfg = mk_cfg(server_url="https://example.invalid")
    cfg.debug_logger = _FakeDebugLogger()

    hooks = _FakeHooks()
    _install_hooks(cfg, hooks)

    response = make_httpx_response(200)
    cfg.async_client = _FakeAsyncClient(response)

    sdk = BaseSDK(cfg)

    captured: dict[str, Any] = {}

    async def fake_retry_async(func: Any, retries: Any) -> Any:
        captured["func"] = func
        captured["retries"] = retries
        return await func()

    monkeypatch.setattr(basesdk_mod.utils, "retry_async", fake_retry_async)

    hook_ctx = _FakeHookCtx(
        config=cfg,
        base_url="https://example.invalid",
        operation_id="unit_test_op",
        oauth2_scopes=[],
        security_source=None,
    )

    res = await sdk.do_request_async(
        hook_ctx=hook_ctx,
        request=object(),
        error_status_codes=["5XX"],
        retry_config=(object(), ["429", "500"]),
    )

    assert res.status_code == 200
    assert "func" in captured and "retries" in captured
    assert hooks.after_success_calls == 1
