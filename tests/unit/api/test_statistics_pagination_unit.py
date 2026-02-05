# tests/unit/api/test_statistics_pagination_unit.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List

import pytest

from dateno.statistics_api import StatisticsAPI
from test_utils import mk_cfg


@dataclass
class _Page:
    items: List[Any]


def _page(items: List[Any]) -> _Page:
    return _Page(items=items)


def test_iter_list_namespaces_increments_start_and_stops(monkeypatch) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    def fake_list_namespaces(*, start=None, limit=None, **kwargs):
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_namespaces", fake_list_namespaces)

    result_pages = list(api.iter_list_namespaces(limit=2, start=0))

    assert len(result_pages) == 1
    assert calls == [(0, 2), (2, 2)]


def test_paginate_list_namespaces_yields_items_across_pages(monkeypatch) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    def fake_list_namespaces(*, start=None, limit=None, **kwargs):
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_namespaces", fake_list_namespaces)

    items = list(api.paginate_list_namespaces(limit=2, start=0))

    assert items == ["a", "b", "c"]
    assert calls == [(0, 2), (2, 2), (4, 2)]


def test_iter_list_indicators_increments_start_and_stops(monkeypatch) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    def fake_list_indicators(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_indicators", fake_list_indicators)

    result_pages = list(api.iter_list_indicators(ns_id="ns", limit=2, start=0))

    assert len(result_pages) == 1
    assert calls == [(0, 2), (2, 2)]


def test_paginate_list_indicators_yields_items_across_pages(monkeypatch) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    def fake_list_indicators(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_indicators", fake_list_indicators)

    items = list(api.paginate_list_indicators(ns_id="ns", limit=2, start=0))

    assert items == ["a", "b", "c"]
    assert calls == [(0, 2), (2, 2), (4, 2)]


def test_iter_list_timeseries_increments_start_and_stops(monkeypatch) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    def fake_list_timeseries(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_timeseries", fake_list_timeseries)

    result_pages = list(api.iter_list_timeseries(ns_id="ns", limit=2, start=0))

    assert len(result_pages) == 1
    assert calls == [(0, 2), (2, 2)]


def test_paginate_list_timeseries_yields_items_across_pages(monkeypatch) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    def fake_list_timeseries(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_timeseries", fake_list_timeseries)

    items = list(api.paginate_list_timeseries(ns_id="ns", limit=2, start=0))

    assert items == ["a", "b", "c"]
    assert calls == [(0, 2), (2, 2), (4, 2)]


@pytest.mark.anyio
async def test_iter_list_namespaces_async_increments_start_and_stops(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    async def fake_list_namespaces_async(*, start=None, limit=None, **kwargs):
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_namespaces_async", fake_list_namespaces_async)

    result_pages = [
        page async for page in api.iter_list_namespaces_async(limit=2, start=0)
    ]

    assert len(result_pages) == 1
    assert calls == [(0, 2), (2, 2)]


@pytest.mark.anyio
async def test_paginate_list_namespaces_async_yields_items_across_pages(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    async def fake_list_namespaces_async(*, start=None, limit=None, **kwargs):
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_namespaces_async", fake_list_namespaces_async)

    items = [
        item async for item in api.paginate_list_namespaces_async(limit=2, start=0)
    ]

    assert items == ["a", "b", "c"]
    assert calls == [(0, 2), (2, 2), (4, 2)]


@pytest.mark.anyio
async def test_iter_list_indicators_async_increments_start_and_stops(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    async def fake_list_indicators_async(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_indicators_async", fake_list_indicators_async)

    result_pages = [
        page async for page in api.iter_list_indicators_async(ns_id="ns", limit=2, start=0)
    ]

    assert len(result_pages) == 1
    assert calls == [(0, 2), (2, 2)]


@pytest.mark.anyio
async def test_paginate_list_indicators_async_yields_items_across_pages(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    async def fake_list_indicators_async(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_indicators_async", fake_list_indicators_async)

    items = [
        item
        async for item in api.paginate_list_indicators_async(
            ns_id="ns", limit=2, start=0
        )
    ]

    assert items == ["a", "b", "c"]
    assert calls == [(0, 2), (2, 2), (4, 2)]


@pytest.mark.anyio
async def test_iter_list_timeseries_async_increments_start_and_stops(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page([1, 2]), _page([])]

    async def fake_list_timeseries_async(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_timeseries_async", fake_list_timeseries_async)

    result_pages = [
        page async for page in api.iter_list_timeseries_async(ns_id="ns", limit=2, start=0)
    ]

    assert len(result_pages) == 1
    assert calls == [(0, 2), (2, 2)]


@pytest.mark.anyio
async def test_paginate_list_timeseries_async_yields_items_across_pages(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())
    calls: list[tuple[int | None, int | None]] = []
    pages = [_page(["a", "b"]), _page(["c"]), _page([])]

    async def fake_list_timeseries_async(*, ns_id, start=None, limit=None, **kwargs):
        assert ns_id == "ns"
        calls.append((start, limit))
        return pages.pop(0)

    monkeypatch.setattr(api, "list_timeseries_async", fake_list_timeseries_async)

    items = [
        item
        async for item in api.paginate_list_timeseries_async(
            ns_id="ns", limit=2, start=0
        )
    ]

    assert items == ["a", "b", "c"]
    assert calls == [(0, 2), (2, 2), (4, 2)]
