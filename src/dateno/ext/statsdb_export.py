from __future__ import annotations

from pathlib import Path
from typing import Optional, Mapping

from dateno.apis.statistics_api import StatisticsAPI, ExportTimeseriesFileAcceptEnum


def export_timeseries_file_bytes(
    stats: StatisticsAPI,
    *,
    ns_id: str,
    ts_id: str,
    fileext: str,
    accept: Optional[ExportTimeseriesFileAcceptEnum] = None,
    timeout_ms: Optional[int] = None,
    http_headers: Optional[Mapping[str, str]] = None,
) -> bytes:
    """
    Reliable helper for streamed exports.
    - Calls generated export_timeseries_file(stream=True)
    - Ensures response is read
    - Returns bytes
    """
    resp = stats.export_timeseries_file(
        ns_id=ns_id,
        ts_id=ts_id,
        fileext=fileext,
        accept_header_override=accept,
        timeout_ms=timeout_ms,
        http_headers=http_headers,
    )

    r = resp.result  # httpx.Response
    # Important: streamed response must be read before accessing content
    if hasattr(r, "read"):
        r.read()

    # After read(), .content is available
    return r.content


def export_timeseries_file_to_path(
    stats: StatisticsAPI,
    *,
    ns_id: str,
    ts_id: str,
    fileext: str,
    path: str | Path,
    accept: Optional[ExportTimeseriesFileAcceptEnum] = None,
    timeout_ms: Optional[int] = None,
    http_headers: Optional[Mapping[str, str]] = None,
) -> Path:
    data = export_timeseries_file_bytes(
        stats,
        ns_id=ns_id,
        ts_id=ts_id,
        fileext=fileext,
        accept=accept,
        timeout_ms=timeout_ms,
        http_headers=http_headers,
    )
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return p
