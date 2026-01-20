"""
Unit tests for the `DataCatalogsAPI` client (sync + async).

Scope:
    These tests validate SDK *client-side* behavior only:
      - request construction (HTTP method + path)
      - correct operation_id passed into hook context
      - correct response unmarshalling branch for a successful 200 response

Non-goals:
    - end-to-end HTTP transport behavior (covered by integration tests)
    - correctness of `dateno.utils.match_response` (we patch it with a deterministic fake)

Approach:
    We patch:
      - `_build_request` / `_build_request_async` to capture request parameters
      - `do_request` / `do_request_async` to return a controlled FakeResponse
      - `dateno.utils.match_response` to ensure deterministic matching
      - `dateno.data_catalogs_api.unmarshal_json_response` to avoid coupling to models

This keeps the tests stable across regenerated SDK code and focuses on
the observable contract of each API method.
"""

from __future__ import annotations

from typing import Any

import pytest

import dateno.data_catalogs_api as mod
from test_utils import (
    FakeResponse,
    assert_request_common,
    make_unmarshal_json_response_stub,
    patch_match_response,
)


@pytest.fixture()
def api(sdk):
    """
    Provide the `DataCatalogsAPI` client from the shared SDK fixture.

    Notes:
        The `sdk` fixture is defined in `tests/conftest.py` and is responsible
        for configuring server URL / API key and managing HTTP client lifecycle.
    """
    return sdk.data_catalogs_api


def test_get_catalog_by_id_builds_request_and_parses_200(monkeypatch, api) -> None:
    """
    Ensure `get_catalog_by_id()` builds a GET request to the expected path and
    unmarshals a 200 JSON response.

    Validates:
        - `_build_request` receives method/path/base_url
        - `do_request` receives a HookContext with operation_id="get_catalog_by_id"
        - `unmarshal_json_response` is called and its return value is returned
    """
    captured: dict[str, Any] = {}

    def fake_build_request(**kwargs):
        captured["build"] = {
            "method": kwargs.get("method"),
            "path": kwargs.get("path"),
            "base_url": kwargs.get("base_url"),
            "request_type": type(kwargs.get("request")).__name__,
        }
        return object()

    def fake_do_request(**kwargs):
        hook_ctx = kwargs.get("hook_ctx")
        captured["do"] = {
            "operation_id": getattr(hook_ctx, "operation_id", None),
            "error_status_codes": kwargs.get("error_status_codes"),
        }
        return FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b'{"ok":true}',
        )

    monkeypatch.setattr(api, "_build_request", fake_build_request)
    monkeypatch.setattr(api, "do_request", fake_do_request)

    # Deterministic matcher: we do not want tests to depend on production matcher logic.
    patch_match_response(monkeypatch)

    # Decouple from model validation: return a stable payload for the expected model type.
    unmarshal_stub = make_unmarshal_json_response_stub(
        {
            "DataCatalog": {"ok": True},
            # Fallback in case regenerated SDK uses a different name/typing wrapper.
            # (Still safe because the stub will raise for unexpected types.)
        }
    )
    monkeypatch.setattr(mod, "unmarshal_json_response", unmarshal_stub)

    result = api.get_catalog_by_id(catalog_id="wb")

    assert result == {"ok": True}
    assert_request_common(
        captured["build"],
        method="GET",
        path="/registry/catalog/{catalog_id}",
    )
    assert captured["do"]["operation_id"] == "get_catalog_by_id"
    # Speakeasy SDK generally configures these error codes for the operation.
    assert captured["do"]["error_status_codes"] is not None


def test_list_catalogs_builds_request_and_parses_200(monkeypatch, api) -> None:
    """
    Ensure `list_catalogs()` builds a GET request to the expected path and
    unmarshals a 200 JSON response.

    Validates:
        - `_build_request` receives method/path
        - `do_request` receives operation_id="list_catalogs"
        - return value comes from `unmarshal_json_response`
    """
    captured: dict[str, Any] = {}

    def fake_build_request(**kwargs):
        captured["build"] = {
            "method": kwargs.get("method"),
            "path": kwargs.get("path"),
        }
        return object()

    def fake_do_request(**kwargs):
        hook_ctx = kwargs.get("hook_ctx")
        captured["do"] = {"operation_id": getattr(hook_ctx, "operation_id", None)}
        return FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b'{"items":[]}',
        )

    monkeypatch.setattr(api, "_build_request", fake_build_request)
    monkeypatch.setattr(api, "do_request", fake_do_request)

    patch_match_response(monkeypatch)

    # Response type is typically a "search response" model (e.g. DataCatalogSearchResponse).
    unmarshal_stub = make_unmarshal_json_response_stub(
        {
            "DataCatalogSearchResponse": {"ok": True},
        }
    )
    monkeypatch.setattr(mod, "unmarshal_json_response", unmarshal_stub)

    result = api.list_catalogs()

    assert result == {"ok": True}
    assert_request_common(
        captured["build"],
        method="GET",
        path="/registry/search/catalogs/",
    )
    assert captured["do"]["operation_id"] == "list_catalogs"


@pytest.mark.anyio
async def test_get_catalog_by_id_async_builds_request_and_parses_200(monkeypatch, api) -> None:
    """
    Ensure `get_catalog_by_id_async()` builds a GET request to the expected path and
    unmarshals a 200 JSON response.

    Validates:
        - `_build_request_async` receives method/path
        - `do_request_async` receives operation_id="get_catalog_by_id"
        - return value comes from `unmarshal_json_response`
    """
    captured: dict[str, Any] = {}

    def fake_build_request_async(**kwargs):
        captured["build"] = {"method": kwargs.get("method"), "path": kwargs.get("path")}
        return object()

    async def fake_do_request_async(**kwargs):
        hook_ctx = kwargs.get("hook_ctx")
        captured["do"] = {"operation_id": getattr(hook_ctx, "operation_id", None)}
        return FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b'{"ok":true}',
        )

    monkeypatch.setattr(api, "_build_request_async", fake_build_request_async)
    monkeypatch.setattr(api, "do_request_async", fake_do_request_async)

    patch_match_response(monkeypatch)

    unmarshal_stub = make_unmarshal_json_response_stub(
        {
            "DataCatalog": {"async": True},
        }
    )
    monkeypatch.setattr(mod, "unmarshal_json_response", unmarshal_stub)

    result = await api.get_catalog_by_id_async(catalog_id="wb")

    assert result == {"async": True}
    assert_request_common(
        captured["build"],
        method="GET",
        path="/registry/catalog/{catalog_id}",
    )
    assert captured["do"]["operation_id"] == "get_catalog_by_id"


@pytest.mark.anyio
async def test_list_catalogs_async_builds_request_and_parses_200(monkeypatch, api) -> None:
    """
    Ensure `list_catalogs_async()` builds a GET request to the expected path and
    unmarshals a 200 JSON response.

    Validates:
        - `_build_request_async` receives method/path
        - `do_request_async` receives operation_id="list_catalogs"
        - return value comes from `unmarshal_json_response`
    """
    captured: dict[str, Any] = {}

    def fake_build_request_async(**kwargs):
        captured["build"] = {"method": kwargs.get("method"), "path": kwargs.get("path")}
        return object()

    async def fake_do_request_async(**kwargs):
        hook_ctx = kwargs.get("hook_ctx")
        captured["do"] = {"operation_id": getattr(hook_ctx, "operation_id", None)}
        return FakeResponse(
            200,
            headers={"Content-Type": "application/json"},
            content=b'{"items":[]}',
        )

    monkeypatch.setattr(api, "_build_request_async", fake_build_request_async)
    monkeypatch.setattr(api, "do_request_async", fake_do_request_async)

    patch_match_response(monkeypatch)

    unmarshal_stub = make_unmarshal_json_response_stub(
        {
            "DataCatalogSearchResponse": {"async": True},
        }
    )
    monkeypatch.setattr(mod, "unmarshal_json_response", unmarshal_stub)

    result = await api.list_catalogs_async()

    assert result == {"async": True}
    assert_request_common(
        captured["build"],
        method="GET",
        path="/registry/search/catalogs/",
    )
    assert captured["do"]["operation_id"] == "list_catalogs"
