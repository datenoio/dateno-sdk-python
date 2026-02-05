# tests/unit/api/test_service_timeout_unit.py
from __future__ import annotations

import httpx
import pytest

import dateno.service as service_mod
from dateno import errors
from dateno.service import Service
from test_utils import FakeResponse, mk_cfg, patch_match_response


def _patch_service_success(monkeypatch, service: Service) -> None:
    patch_match_response(monkeypatch)
    monkeypatch.setattr(
        service_mod,
        "unmarshal_json_response",
        lambda *args, **kwargs: {"ok": True},
    )
    monkeypatch.setattr(
        service,
        "do_request",
        lambda **kwargs: FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b"{}",
        ),
    )


def _patch_service_success_async(monkeypatch, service: Service) -> None:
    patch_match_response(monkeypatch)
    monkeypatch.setattr(
        service_mod,
        "unmarshal_json_response",
        lambda *args, **kwargs: {"ok": True},
    )

    async def _do_request_async(**kwargs):
        return FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b"{}",
        )

    monkeypatch.setattr(service, "do_request_async", _do_request_async)


def test_get_healthz_uses_default_timeout_ms(monkeypatch) -> None:
    cfg = mk_cfg()
    service = Service(cfg)
    captured: dict[str, object] = {}

    def fake_build_request(**kwargs):
        captured["timeout_ms"] = kwargs.get("timeout_ms")
        return object()

    monkeypatch.setattr(service, "_build_request", fake_build_request)
    _patch_service_success(monkeypatch, service)

    result = service.get_healthz()

    assert result == {"ok": True}
    assert captured["timeout_ms"] == cfg.timeout_ms


def test_get_healthz_uses_timeout_override(monkeypatch) -> None:
    cfg = mk_cfg()
    service = Service(cfg)
    captured: dict[str, object] = {}

    def fake_build_request(**kwargs):
        captured["timeout_ms"] = kwargs.get("timeout_ms")
        return object()

    monkeypatch.setattr(service, "_build_request", fake_build_request)
    _patch_service_success(monkeypatch, service)

    service.get_healthz(timeout_ms=1234)

    assert captured["timeout_ms"] == 1234


@pytest.mark.anyio
async def test_get_healthz_async_uses_default_timeout_ms(monkeypatch) -> None:
    cfg = mk_cfg()
    service = Service(cfg)
    captured: dict[str, object] = {}

    def fake_build_request_async(**kwargs):
        captured["timeout_ms"] = kwargs.get("timeout_ms")
        return object()

    monkeypatch.setattr(service, "_build_request_async", fake_build_request_async)
    _patch_service_success_async(monkeypatch, service)

    result = await service.get_healthz_async()

    assert result == {"ok": True}
    assert captured["timeout_ms"] == cfg.timeout_ms


@pytest.mark.anyio
async def test_get_healthz_async_uses_timeout_override(monkeypatch) -> None:
    cfg = mk_cfg()
    service = Service(cfg)
    captured: dict[str, object] = {}

    def fake_build_request_async(**kwargs):
        captured["timeout_ms"] = kwargs.get("timeout_ms")
        return object()

    monkeypatch.setattr(service, "_build_request_async", fake_build_request_async)
    _patch_service_success_async(monkeypatch, service)

    await service.get_healthz_async(timeout_ms=4321)

    assert captured["timeout_ms"] == 4321


def test_get_healthz_unexpected_response_includes_body(monkeypatch) -> None:
    cfg = mk_cfg()
    service = Service(cfg)

    monkeypatch.setattr(service, "_build_request", lambda **kwargs: object())

    def fake_do_request(**kwargs):
        req = httpx.Request("GET", "https://example.invalid/healthz")
        return httpx.Response(
            418,
            headers={"Content-Type": "text/plain"},
            content=b"weird-body",
            request=req,
        )

    monkeypatch.setattr(service, "do_request", fake_do_request)
    monkeypatch.setattr(service_mod.utils, "match_response", lambda *args, **kwargs: False)

    with pytest.raises(errors.SDKDefaultError) as exc_info:
        service.get_healthz()

    assert "weird-body" in str(exc_info.value)


@pytest.mark.anyio
async def test_get_healthz_async_unexpected_response_includes_body(
    monkeypatch,
) -> None:
    cfg = mk_cfg()
    service = Service(cfg)

    monkeypatch.setattr(service, "_build_request_async", lambda **kwargs: object())

    async def fake_do_request_async(**kwargs):
        req = httpx.Request("GET", "https://example.invalid/healthz")
        return httpx.Response(
            418,
            headers={"Content-Type": "text/plain"},
            content=b"weird-body-async",
            request=req,
        )

    monkeypatch.setattr(service, "do_request_async", fake_do_request_async)
    monkeypatch.setattr(service_mod.utils, "match_response", lambda *args, **kwargs: False)

    with pytest.raises(errors.SDKDefaultError) as exc_info:
        await service.get_healthz_async()

    assert "weird-body-async" in str(exc_info.value)
