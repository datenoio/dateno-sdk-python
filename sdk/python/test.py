#!/usr/bin/env python3
"""
Smoke test: statsdb SDK methods against https://api.test.dateno.io

Env:
  DATENO_SERVER_URL   default: https://api.test.dateno.io
  DATENO_APIKEY       required (query param)

Run:
  DATENO_APIKEY=... python smoke_statsdb_problematic.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Iterable, Optional


def _env(name: str, default: Optional[str] = None) -> Optional[str]:
    v = os.getenv(name)
    return default if not v else v


def _pick_attr(obj: Any, candidates: Iterable[str], *, what: str) -> Any:
    for name in candidates:
        if hasattr(obj, name):
            return getattr(obj, name)
    raise AttributeError(f"Cannot find {what}. Tried: {', '.join(candidates)}")


def _call(obj: Any, method: str, /, **kwargs) -> Any:
    fn = getattr(obj, method, None)
    if not callable(fn):
        raise AttributeError(f"Method not found: {obj.__class__.__name__}.{method}")
    return fn(**kwargs)


def _iter_public_attrs(obj: Any) -> Iterable[str]:
    # Avoid dunder; include single underscore attrs rarely needed for speakeasy
    for name in dir(obj):
        if name.startswith("__"):
            continue
        yield name


# def _bytes_from_export_response(resp: Any) -> bytes:
#     """
#     Extract file bytes from Speakeasy operation response.
#
#     Handles patterns:
#       - Speakeasy wrapper: resp.result -> httpx.Response
#       - httpx.Response streaming (ResponseNotRead): must call resp.read()
#       - requests.Response: resp.content available
#     """
#     if resp is None:
#         raise RuntimeError("Export response is None")
#
#     # 0) Speakeasy wrapper stores the actual HTTP response in `.result`
#     inner = getattr(resp, "result", None)
#     if inner is not None:
#         return _bytes_from_export_response(inner)
#
#     # 1) If this is a streaming httpx.Response, calling `.content` raises ResponseNotRead.
#     # Prefer `.read()` when present.
#     read = getattr(resp, "read", None)
#     if callable(read):
#         data = read()
#         # httpx.Response.read() is sync and returns bytes.
#         # If it returns a coroutine, then we're in async world.
#         if hasattr(data, "__await__"):
#             raise RuntimeError(
#                 "Got async streaming response (read() returned coroutine). "
#                 "This smoke test is synchronous; use AsyncClient/asyncio to read the body."
#             )
#         if isinstance(data, (bytes, bytearray)):
#             return bytes(data)
#
#     # 2) Standard `.content` (requests.Response, or already-read httpx.Response)
#     try:
#         content = getattr(resp, "content", None)
#         if isinstance(content, (bytes, bytearray)):
#             return bytes(content)
#     except Exception:
#         # e.g. httpx.ResponseNotRead - we'll try other fallbacks below
#         pass
#
#     # 3) Streaming iterator fallback (may work for already-open responses)
#     iter_bytes = getattr(resp, "iter_bytes", None)
#     if callable(iter_bytes):
#         chunks: list[bytes] = []
#         for chunk in iter_bytes():
#             if isinstance(chunk, (bytes, bytearray)):
#                 chunks.append(bytes(chunk))
#         if chunks:
#             return b"".join(chunks)
#
#     # 4) Text fallback
#     try:
#         text = getattr(resp, "text", None)
#         if isinstance(text, str) and text:
#             return text.encode("utf-8")
#     except Exception:
#         pass
#
#     raise RuntimeError(f"Cannot extract bytes from export response: {type(resp)}")


def _bytes_from_export_response(resp: Any) -> bytes:
    """
    Extract file bytes from Speakeasy operation response.

    Expected shape for this SDK:
      - resp: ExportTimeseriesFileResponse (pydantic)
      - resp.result: httpx.Response (often streaming)
    """
    if resp is None:
        raise RuntimeError("Export response is None")

    # Unwrap Speakeasy pydantic response wrapper
    inner = getattr(resp, "result", None)
    if inner is not None:
        resp = inner  # httpx.Response

    # If it's an httpx.Response, it might be streaming.
    # For streaming responses, you MUST call .read() before accessing .content.
    read = getattr(resp, "read", None)
    if callable(read):
        data = read()
        # In sync httpx, read() returns bytes. If it returns coroutine -> async response.
        if hasattr(data, "__await__"):
            raise RuntimeError(
                "Got async streaming response (read() returned coroutine). "
                "This smoke test is synchronous."
            )
        if isinstance(data, (bytes, bytearray)):
            return bytes(data)
        # Some implementations return None but still populate resp.content after read()
        # fall through to .content below

    # After read(), .content should be accessible
    content = getattr(resp, "content", None)
    if isinstance(content, (bytes, bytearray)):
        return bytes(content)

    # As a last resort, try .text (shouldn't normally be needed for csv)
    text = getattr(resp, "text", None)
    if isinstance(text, str) and text:
        return text.encode("utf-8")

    raise RuntimeError(f"Cannot extract bytes from export response: {type(resp)}")


def _classify_exception(e: Exception) -> str:
    """
    Speakeasy typically throws ErrorResponse (custom) for non-2xx.
    We classify via status_code if present.
    """
    status_code = getattr(e, "status_code", None)
    if isinstance(status_code, int):
        if 400 <= status_code <= 499:
            return "4XX"
        if 500 <= status_code <= 599:
            return "5XX"
    return "OTHER"


def _print_error_details(e: Exception) -> None:
    status_code = getattr(e, "status_code", None)
    if isinstance(status_code, int):
        print("  status_code:", status_code)

    # Speakeasy ErrorResponse often has .data.detail
    detail = None
    data = getattr(e, "data", None)
    if data is not None:
        detail = getattr(data, "detail", None)

    # or .body is json string
    body = getattr(e, "body", None)
    if detail:
        print("  detail:", detail)
    elif isinstance(body, str) and body:
        print("  body:", body[:300])

    headers = getattr(e, "headers", None)
    if headers is not None:
        # headers might be httpx.Headers
        try:
            trace = headers.get("x-trace-id")
            reqid = headers.get("x-request-id")
            if trace:
                print("  x-trace-id:", trace)
            if reqid:
                print("  x-request-id:", reqid)
        except Exception:
            pass


def main() -> int:
    server_url = _env("DATENO_SERVER_URL", "https://api.test.dateno.io")
    apikey = _env("DATENO_APIKEY", 'ovTReiGfgOjUNrMKCWYmisqxJXuTy8dL')
    if not apikey:
        print("ERROR: DATENO_APIKEY is required", file=sys.stderr)
        return 2

    from dateno import SDK  # Speakeasy entrypoint

    sdk = SDK(server_url=server_url, api_key_query=apikey)
    print(f"Using server_url={server_url}")

    stats = _pick_attr(
        sdk,
        ["statistics_api", "statsdb_api", "stats_api", "statistics"],
        what="statsdb/statistics api",
    )

    # 1) list_namespaces
    print("\n=== list_namespaces ===")
    try:
        ns_page = _call(stats, "list_namespaces", limit=10)
        ns_items = getattr(ns_page, "items", []) or []
        print("[OK] list_namespaces; items:", len(ns_items))
    except Exception as e:
        print("[FAIL] list_namespaces:", repr(e))
        return 1

    ns_id = "ilostat"

    # 2) get_namespace
    print("\n=== get_namespace ===")
    try:
        ns_obj = _call(stats, "get_namespace", ns_id=ns_id)
        md = getattr(ns_obj, "metadata", None)
        print("[OK] get_namespace id=", getattr(ns_obj, "id", None))
        print("metadata_type:", type(md).__name__)
    except Exception as e:
        print("[FAIL] get_namespace:", repr(e))

    # 3) list_indicators
    print("\n=== list_indicators ===")
    try:
        ind_page = _call(stats, "list_indicators", ns_id=ns_id, limit=10)
        ind_items = getattr(ind_page, "items", []) or []
        print("[OK] list_indicators; items:", len(ind_items))
    except Exception as e:
        print("[FAIL] list_indicators:", repr(e))

    # 4) list_timeseries
    print("\n=== list_timeseries ===")
    ts_page = None
    try:
        ts_page = _call(stats, "list_timeseries", ns_id=ns_id, limit=10)
        ts_items = getattr(ts_page, "items", []) or []
        print("[OK] list_timeseries; items:", len(ts_items))
    except Exception as e:
        print("[FAIL] list_timeseries:", repr(e))
        ts_items = []

    # Export test for several ts_id
    out_dir = Path("/tmp/exports")
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\n=== export_timeseries_file (try first 10 ts_id) ===")
    ok = err4 = err5 = other = 0

    for i, ts in enumerate(ts_items[:10], start=1):
        ts_id = getattr(ts, "id", None)
        if not ts_id:
            print(f"\n-- [{i}/10] ts_id=<missing> -> skip")
            other += 1
            continue

        out_path = out_dir / f"{ns_id}__{ts_id}.csv"
        print(f"\n-- [{i}/10] ts_id={ts_id} -> {out_path}")

        try:
            resp = stats.export_timeseries_file(ns_id=ns_id, ts_id=ts_id, fileext="csv")
            data = _bytes_from_export_response(resp)
            out_path.write_bytes(data)
            print("[OK] bytes:", len(data))
            ok += 1
        except Exception as e:
            cls = _classify_exception(e)
            if cls == "4XX":
                err4 += 1
                print("[FAIL:4XX]:", repr(e))
                _print_error_details(e)
            elif cls == "5XX":
                err5 += 1
                print("[FAIL:5XX]:", repr(e))
                _print_error_details(e)
            else:
                other += 1
                print("[FAIL:OTHER]:", repr(e))

    print("\n=== export summary ===")
    print("OK:", ok)
    print("4XX:", err4)
    print("5XX:", err5)
    print("OTHER:", other)

    # Control: expected 4XX
    print("\n=== export_timeseries_file (expected 4XX control) ===")
    try:
        stats.export_timeseries_file(
            ns_id=ns_id,
            ts_id="__definitely_not_existing__",
            fileext="csv",
        )
        print("[UNEXPECTED] export succeeded for invalid ts_id")
    except Exception as e:
        cls = _classify_exception(e)
        if cls == "4XX":
            print("[OK] got expected error for invalid ts_id:", repr(e))
            _print_error_details(e)
        else:
            print("[FAIL] expected 4XX, got:", repr(e))
            _print_error_details(e)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
