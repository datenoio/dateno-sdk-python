#!/usr/bin/env python3
"""
SDK smoke tests (curl-like coverage)

Env:
  DATENO_SERVER_URL   default: https://api.test.dateno.io
  DATENO_APIKEY       required for almost all endpoints

Run:
  DATENO_APIKEY=... python smoke_sdk_all.py
  DATENO_SERVER_URL=http://127.0.0.1:8100 DATENO_APIKEY=... python smoke_sdk_all.py
"""

from __future__ import annotations

import os
import sys
from typing import Any, Iterable, Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    if v is None or v == "":
        return default
    return v


def _pick_attr(obj: Any, candidates: Iterable[str], *, what: str) -> Any:
    for name in candidates:
        if hasattr(obj, name):
            return getattr(obj, name)
    raise AttributeError(f"Cannot find {what}. Tried: {', '.join(candidates)}")


def _call(obj: Any, method_candidates: Iterable[str], /, **kwargs) -> Any:
    for name in method_candidates:
        fn = getattr(obj, name, None)
        if callable(fn):
            return fn(**kwargs)
    raise AttributeError(
        f"Cannot find method on {obj.__class__.__name__}. Tried: {', '.join(method_candidates)}"
    )


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    server_url = _env("DATENO_SERVER_URL", "https://api.test.dateno.io")
    apikey = _env("DATENO_APIKEY")

    if not apikey:
        print("ERROR: DATENO_APIKEY is required", file=sys.stderr)
        return 2

    # --- SDK init (apikey via query only; bearer intentionally omitted) ---
    from dateno.sdk import SDK
    from dateno import models

    sdk = SDK(
        server_url=server_url,
        api_key_query=apikey,
    )

    print(f"Using server_url={server_url}")

    # -------------------
    # 1) /healthz
    # -------------------
    svc = _pick_attr(sdk, ["service", "service_api"], what="service api")
    health = _call(svc, ["get_healthz", "healthz", "get_health"],)
    _assert(isinstance(health, dict), "healthz: expected dict-like response")
    _assert(health.get("status") == "ok", f"healthz: expected status=ok, got {health}")
    _assert(health.get("elasticsearch") is True, f"healthz: expected elasticsearch=True, got {health}")
    print("[OK] service.get_healthz")

    # -------------------
    # 2) /registry/catalog/{catalog_id}
    # 3) /registry/search/catalogs/?q=...&limit=...&offset=...
    # -------------------
    catalog_api = _pick_attr(
        sdk,
        [
            "data_catalogs_api",
            "catalog_api",
            "registry_api",
            "catalogs_api",
        ],
        what="catalog/registry api",
    )

    # --- (2) single catalog by UID
    catalog_id = "cdi00001616"
    cat = _call(
        catalog_api,
        [
            "get_catalog_by_id",        # preferred operation_id naming
            "fetch_single_catalog",     # router handler name
            "get_catalog",              # generic SDK naming
            "get_registry_catalog",     # alternative naming
        ],
        catalog_id=catalog_id,
    )
    _assert(cat is not None, "registry/catalog: expected non-empty response")
    print("[OK] catalog.get_catalog_by_id")

    # --- (3) search catalogs
    cats = _call(
        catalog_api,
        [
            "search_catalogs",          # router handler name (likely)
            "list_catalogs",            # alternative operation_id naming
            "search_data_catalogs",     # alternative SDK naming
        ],
        q="environment",
        limit=10,
        offset=0,
    )

    # IMPORTANT: This endpoint returns DataCatalogSearchResponse: { meta, data }
    data = getattr(cats, "data", None)
    if data is None and isinstance(cats, dict):
        data = cats.get("data")

    _assert(data is not None, "registry/search/catalogs: response has no data field")
    _assert(isinstance(data, list), "registry/search/catalogs: data must be a list")

    print(f"[OK] catalog.search_catalogs (data={len(data)})")


    # -------------------
    # 4) /search/0.2/query
    # 5) /search/0.1/entry/{entry_id}
    # 6) POST /search/0.2/es_search
    # 7) /search/0.2/list_facets
    # 8) /search/0.2/get_facet?key=...
    # 9) /search/0.2/similar/{entry_id}
    # -------------------
    search_api = _pick_attr(sdk, ["search_api", "search"], what="search api")

    q = _call(
        search_api,
        [
            "search_datasets",          # your current SDK method
            "query",                   # possible SDK naming
            "search_query",            # possible SDK naming
        ],
        q="environment",
        limit=1,
        offset=0,
        facets=True,
        sort_by="_score",
    )
    total_val = getattr(getattr(getattr(q, "hits", None), "total", None), "value", None)
    _assert(total_val is None or total_val >= 1, f"search/query: expected total>=1, got {q}")
    print("[OK] search.search_datasets (/search/0.2/query)")

    # pick entry_id from first hit if possible, else use your known id
    entry_id = "89dab920d0ff1f03ae44885e7ff021358cb0f531cc81b61579f06b0d4ff4ee28"
    try:
        hits = getattr(getattr(q, "hits", None), "hits", None)
        if hits and len(hits) > 0:
            # Speakeasy-style: Hit(id=..., source=...)
            entry_id = getattr(hits[0], "id", entry_id) or entry_id
    except Exception:
        pass

    entry = _call(
        search_api,
        [
            "get_dataset_by_entry_id",
            "fetch_single_entry",       # common naming in older drafts
            "get_entry",                # possible naming
            "get_search_entry",         # possible naming
            "get_entry_by_id",          # possible naming
        ],
        entry_id=entry_id,
    )
    _assert(entry is not None, "search/entry: expected non-empty response")
    print("[OK] search.get_entry (/search/0.1/entry/{entry_id})")

    es = _call(
        search_api,
        [
            "search_datasets_dsl",
            "es_search",
            "post_es_search",
            "search_es",
        ],
        limit=1,
        offset=0,
        facets=True,
        sortby="_score",
        body={  # <-- ключевой момент: единый request body
            "query": {"match_all": {}},
            # "post_filter": {"term": {"source.catalog_type": {"value": "Geoportal"}}},  # если нужно
        },
    )
    es_total = getattr(getattr(getattr(es, "hits", None), "total", None), "value", None)
    _assert(es_total is None or es_total >= 0, f"search/es_search: unexpected response {es}")
    print("[OK] search.es_search (POST /search/0.2/es_search)")

    facets = _call(
        search_api,
        [
            "list_search_facets",
            "get_facets",
        ],
    )
    _assert(facets is not None, "search/list_facets: expected non-empty response")
    print("[OK] search.list_facets")

    facet_key = "source.catalog_type"
    facet = _call(
        search_api,
        [
            "get_search_facet_values",
            "facet",
        ],
        key=facet_key,
    )
    _assert(facet is not None, "search/get_facet: expected non-empty response")
    print("[OK] search.get_facet")

    similar = _call(
        search_api,
        [
            "get_similar_datasets",
            "get_similar",
            "get_similar_entries",
        ],
        entry_id=entry_id,
        limit=5,
    )
    _assert(similar is not None, "search/similar: expected non-empty response")
    print("[OK] search.similar")

    # -------------------
    # 10) /raw/0.1/entry/{entry_id}
    # -------------------
    raw_api = _pick_attr(sdk, ["raw_data_access", "raw", "raw_api"], what="raw api")
    raw_entry = _call(
        raw_api,
        [
            "get_raw_entry_by_id",
            "get_entry",
            "fetch_entry",
            "get_raw_entry",
            "entry",
        ],
        entry_id=entry_id,
    )
    _assert(raw_entry is not None, "raw/entry: expected non-empty response")
    print("[OK] raw.get_entry")

    # -------------------
    # 11) /statsdb/0.1/ns
    # 12) /statsdb/0.1/ns/{ns}
    # 13) /statsdb/0.1/ns/{ns}/tables
    # 14) /statsdb/0.1/ns/{ns}/tables/{table}
    # 15) /statsdb/0.1/ns/{ns}/indicators
    # 16) /statsdb/0.1/ns/{ns}/indicators/{indicator}
    # 17) /statsdb/0.1/ns/{ns}/ts
    # 18) /statsdb/0.1/ns/{ns}/ts/{ts}
    # 19) /statsdb/0.1/list_exportable_formats
    # -------------------
    stats = _pick_attr(
        sdk,
        [
            "statistics_api",
            "statsdb_api",
            "stats_api",
            "statistics",
        ],
        what="statsdb/statistics api",
    )

    ns_page = _call(stats, ["list_namespaces", "list_ns", "namespaces"], limit=10)
    ns_items = getattr(ns_page, "items", None) if ns_page is not None else None
    _assert(ns_items is not None and len(ns_items) >= 1, "statsdb/ns: expected >=1 namespaces")
    ns_id = getattr(ns_items[0], "id", None) or "ilostat"
    print("[OK] stats.list_namespaces")

    ns_obj = _call(stats, ["get_namespace", "get_ns", "namespace"], ns_id=ns_id)
    _assert(ns_obj is not None, "statsdb/ns/{ns}: expected namespace object")
    print("[OK] stats.get_namespace")

    tbl_page = _call(stats, ["list_namespace_tables", "tables"], ns_id=ns_id, limit=10)
    tbl_items = getattr(tbl_page, "items", None)
    _assert(tbl_items is not None and len(tbl_items) >= 1, "statsdb/tables: expected >=1 tables")
    table_id = getattr(tbl_items[0], "id", None) or "CCF_XOXR_CUR_RT_A"
    print("[OK] stats.list_tables")

    table_obj = _call(stats, ["get_namespace_table", "table"], ns_id=ns_id, table_id=table_id)
    _assert(table_obj is not None, "statsdb/table: expected table object")
    print("[OK] stats.get_table")

    ind_page = _call(stats, ["list_indicators", "list_ind", "indicators"], ns_id=ns_id, limit=10)
    ind_items = getattr(ind_page, "items", None)
    _assert(ind_items is not None and len(ind_items) >= 1, "statsdb/indicators: expected >=1 indicators")
    ind_id = getattr(ind_items[0], "id", None) or "CLD_TPOP_SEX_AGE_NB"
    print("[OK] stats.list_indicators")

    ind_obj = _call(stats, ["get_namespace_indicator", "get_ind", "indicator"], ns_id=ns_id, ind_id=ind_id)
    _assert(ind_obj is not None, "statsdb/indicator: expected indicator object")
    print("[OK] stats.get_indicator")

    ts_page = _call(stats, ["list_timeseries", "list_ts", "timeseries"], ns_id=ns_id, limit=10)
    ts_items = getattr(ts_page, "items", None)
    _assert(ts_items is not None and len(ts_items) >= 1, "statsdb/ts: expected >=1 timeseries")
    ts_id = getattr(ts_items[0], "id", None) or "CCF_XOXR_CUR_RT.ABW"
    print("[OK] stats.list_timeseries")

    ts_obj = _call(stats, ["get_timeseries", "get_ts", "timeseries_by_id"], ns_id=ns_id, ts_id=ts_id)
    _assert(ts_obj is not None, "statsdb/ts/{ts}: expected timeseries object")
    print("[OK] stats.get_timeseries")

    exts = _call(stats, ["list_export_formats", "exportable_formats", "list_formats"])
    _assert(exts is not None, "statsdb/list_exportable_formats: expected non-empty response")
    print("[OK] stats.list_exportable_formats")

    print("\nALL OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
