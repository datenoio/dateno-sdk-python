# tests/unit/api/test_search_pagination_unit.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

import pytest

from dateno.search_api import SearchAPI
from test_utils import mk_cfg


@dataclass
class _FakeHits:
    hits: List[Any]


@dataclass
class _FakeSearchResponse:
    hits: _FakeHits


def _page(items: List[Any]) -> _FakeSearchResponse:
    return _FakeSearchResponse(hits=_FakeHits(hits=items))


def test_iter_search_datasets_pages_increments_offset_and_stops(monkeypatch) -> None:
    api = SearchAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    def fake_search_datasets(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "search_datasets", fake_search_datasets)

    result_pages = list(api.iter_search_datasets(q="env", limit=2, offset=0))

    assert len(result_pages) == 1
    assert calls == [(2, 0), (2, 2)]


def test_paginate_search_datasets_yields_hits_across_pages(monkeypatch) -> None:
    api = SearchAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    def fake_search_datasets(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "search_datasets", fake_search_datasets)

    hits = list(api.paginate_search_datasets(q="env", limit=2, offset=0))

    assert hits == ["a", "b", "c"]
    assert calls == [(2, 0), (2, 2), (2, 4)]


@pytest.mark.anyio
async def test_iter_search_datasets_async_pages_increments_offset_and_stops(
    monkeypatch,
) -> None:
    api = SearchAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    async def fake_search_datasets_async(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "search_datasets_async", fake_search_datasets_async)

    result_pages = [
        page
        async for page in api.iter_search_datasets_async(q="env", limit=2, offset=0)
    ]

    assert len(result_pages) == 1
    assert calls == [(2, 0), (2, 2)]


@pytest.mark.anyio
async def test_paginate_search_datasets_async_yields_hits_across_pages(
    monkeypatch,
) -> None:
    api = SearchAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    async def fake_search_datasets_async(*, limit=None, offset=None, **kwargs):
        calls.append((limit, offset))
        return pages.pop(0)

    monkeypatch.setattr(api, "search_datasets_async", fake_search_datasets_async)

    hits = [
        hit
        async for hit in api.paginate_search_datasets_async(q="env", limit=2, offset=0)
    ]

    assert hits == ["a", "b", "c"]
    assert calls == [(2, 0), (2, 2), (2, 4)]
