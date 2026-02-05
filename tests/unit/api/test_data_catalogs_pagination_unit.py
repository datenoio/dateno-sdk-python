# tests/unit/api/test_data_catalogs_pagination_unit.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

import pytest

from dateno.data_catalogs_api import DataCatalogsAPI
from test_utils import mk_cfg


@dataclass
class _CatalogPage:
    data: List[Any]


def _page(items: List[Any]) -> _CatalogPage:
    return _CatalogPage(data=items)


def test_iter_list_catalogs_increments_offset_and_stops(monkeypatch) -> None:
    api = DataCatalogsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    def fake_list_catalogs(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_catalogs", fake_list_catalogs)

    result_pages = list(api.iter_list_catalogs(limit=2, offset=0))

    assert len(result_pages) == 1
    assert calls == [(2, 0), (2, 2)]


def test_paginate_list_catalogs_yields_items_across_pages(monkeypatch) -> None:
    api = DataCatalogsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    def fake_list_catalogs(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_catalogs", fake_list_catalogs)

    items = list(api.paginate_list_catalogs(limit=2, offset=0))

    assert items == ["a", "b", "c"]
    assert calls == [(2, 0), (2, 2), (2, 4)]


@pytest.mark.anyio
async def test_iter_list_catalogs_async_increments_offset_and_stops(
    monkeypatch,
) -> None:
    api = DataCatalogsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    async def fake_list_catalogs_async(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_catalogs_async", fake_list_catalogs_async)

    result_pages = [
        page async for page in api.iter_list_catalogs_async(limit=2, offset=0)
    ]

    assert len(result_pages) == 1
    assert calls == [(2, 0), (2, 2)]


@pytest.mark.anyio
async def test_paginate_list_catalogs_async_yields_items_across_pages(
    monkeypatch,
) -> None:
    api = DataCatalogsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    async def fake_list_catalogs_async(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_catalogs_async", fake_list_catalogs_async)

    items = [
        item async for item in api.paginate_list_catalogs_async(limit=2, offset=0)
    ]

    assert items == ["a", "b", "c"]
    assert calls == [(2, 0), (2, 2), (2, 4)]
