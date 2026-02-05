# tests/unit/api/test_statistics_export_streaming_unit.py
from __future__ import annotations

import pytest

from dateno import errors, utils
from dateno.statistics_api import StatisticsAPI
from dateno.utils.serializers import STREAM_TEXT_LIMIT
from test_utils import mk_cfg


class _StreamingResponse:
    def __init__(self, body: bytes) -> None:
        self.status_code = 418
        self.headers = {"content-type": "application/octet-stream"}
        self._body = body
        self.iterated = 0

    def iter_bytes(self):
        for b in self._body:
            self.iterated += 1
            yield bytes([b])


def test_export_timeseries_file_unexpected_response_uses_limited_body(
    monkeypatch,
) -> None:
    api = StatisticsAPI(mk_cfg())

    body = b"x" * (STREAM_TEXT_LIMIT + 10)
    response = _StreamingResponse(body)

    monkeypatch.setattr(api, "_build_request", lambda **kwargs: object())
    monkeypatch.setattr(api, "do_request", lambda **kwargs: response)
    monkeypatch.setattr(utils, "match_response", lambda *args, **kwargs: False)

    with pytest.raises(errors.SDKDefaultError) as exc_info:
        api.export_timeseries_file(ns_id="ns", ts_id="ts", fileext="csv")

    assert response.iterated == STREAM_TEXT_LIMIT
    assert "x" * 20 in str(exc_info.value)
