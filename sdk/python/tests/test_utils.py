# tests/test_utils.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

import dateno.utils as utils
from dateno.sdkconfiguration import SDKConfiguration


@dataclass
class FakeResponse:
    """
    Minimal fake HTTP response object for unit testing.

    This class intentionally mimics only the subset of an HTTP response
    that is actually used inside the SDK utilities and tests.

    It is designed to be compatible with:
      - dateno.utils.match_response
      - dateno.utils.stream_to_text
      - SDK error-handling paths that expect `.status_code`, `.headers`,
        `.content`, and `.text`.

    Attributes:
        status_code:
            HTTP status code (e.g. 200, 404, 503).

        headers:
            Mapping of HTTP headers. Content-Type is commonly inspected
            by match_response.

        content:
            Raw response body as bytes. Used by stream_to_text and
            exposed via the `.text` property.
    """

    status_code: int
    headers: dict[str, str] | None = None
    content: bytes = b""

    def __post_init__(self) -> None:
        """
        Normalize headers after initialization.

        Ensures that `headers` is always a dictionary, so downstream code
        does not need to perform None checks.
        """
        if self.headers is None:
            self.headers = {}

    @property
    def text(self) -> str:
        """
        Decode response content as UTF-8 text.

        This mirrors typical HTTP client behavior:
        - Attempts UTF-8 decoding
        - Never raises decoding exceptions
        - Falls back to replacement characters if decoding fails
        """
        try:
            return self.content.decode("utf-8", errors="replace")
        except Exception:
            return ""


def match_response_fake(
    http_res: FakeResponse,
    expected_status: Any,
    content_type: str,
) -> bool:
    """
    Deterministic replacement for `dateno.utils.match_response`.

    This helper is intentionally simple and predictable, making it
    suitable for unit tests where full HTTP semantics are unnecessary.

    Supported `expected_status` formats:
      - Exact status: "200", 200
      - List of statuses: ["500", "503"]
      - Status classes: "4XX", "5XX"

    Supported `content_type` formats:
      - Exact prefix match (e.g. "application/json")
      - "*" to accept any content type

    Args:
        http_res:
            FakeResponse instance representing the HTTP response.

        expected_status:
            Expected status code or status class.

        content_type:
            Expected content type or "*" for wildcard.

    Returns:
        True if the response matches the expected status and content type,
        False otherwise.
    """
    code = str(http_res.status_code)

    if isinstance(expected_status, list):
        if code not in [str(x) for x in expected_status]:
            return False
    else:
        expected_status = str(expected_status)
        if expected_status.endswith("XX") and len(expected_status) == 3:
            # Status class matching: "4XX", "5XX"
            if not code or code[0] != expected_status[0]:
                return False
        else:
            if code != expected_status:
                return False

    if content_type == "*":
        return True

    actual = (
        (http_res.headers.get("content-type") or http_res.headers.get("Content-Type") or "")
        .lower()
        .strip()
    )
    return actual.startswith(content_type.lower())


def patch_match_response(monkeypatch) -> None:
    """
    Patch `dateno.utils.match_response` with the deterministic fake version.

    This helper should be used in unit tests to:
      - Avoid coupling tests to the real match_response implementation
      - Ensure predictable behavior across SDK versions
      - Focus tests on SDK logic rather than HTTP semantics
    """
    monkeypatch.setattr(utils, "match_response", match_response_fake)


def mk_cfg(server_url: str = "https://example.invalid") -> SDKConfiguration:
    """
    Create a minimal SDKConfiguration for unit tests.

    This configuration intentionally:
      - Does NOT create real HTTP clients
      - Marks clients as "supplied" to prevent automatic closing
      - Is suitable for tests that mock `_build_request` or `do_request`

    Args:
        server_url:
            Base server URL to embed into the configuration.

    Returns:
        A lightweight SDKConfiguration instance for unit testing.
    """
    return SDKConfiguration(
        server_url=server_url,
        client=None,
        client_supplied=True,
        async_client=None,
        async_client_supplied=True,
        debug_logger=None,
    )


def make_unmarshal_json_response_stub(
    mapping: Mapping[Any, Any | Callable[[Any], Any]]
) -> Callable[[Any, Any], Any]:
    """
    Build a stub for `unmarshal_json_response`.

    The returned function matches the Speakeasy SDK signature:
        unmarshal_json_response(model_type, raw_response)

    The behavior is controlled via a mapping where:
      - Keys are model classes or model class names
      - Values are either:
          * A static payload to return
          * A callable that derives the payload from raw_response

    Args:
        mapping:
            Mapping of model identifiers to payloads or factories.

    Returns:
        A callable suitable for monkeypatching `unmarshal_json_response`.

    Raises:
        AssertionError if an unexpected model type is requested.
    """

    def _stub(typ: Any, raw_response: Any) -> Any:
        key = typ
        if key not in mapping:
            key = getattr(typ, "__name__", typ)

        if key not in mapping:
            raise AssertionError(
                f"Unexpected response type for unmarshal_json_response: {typ!r}. "
                f"Known keys: {list(mapping.keys())!r}"
            )

        value = mapping[key]
        return value(raw_response) if callable(value) else value

    return _stub


def assert_request_common(
    captured: Mapping[str, Any],
    *,
    method: str,
    path: str,
    base_url: str | None = None,
    request_type: str | None = None,
) -> None:
    """
    Common assertions for captured `_build_request` arguments.

    This helper centralizes repeated checks across SDK API tests and
    ensures consistency when validating request construction.

    Args:
        captured:
            Mapping of captured arguments from a mocked `_build_request`.

        method:
            Expected HTTP method (e.g. "GET", "POST").

        path:
            Expected request path (e.g. "/healthz").

        base_url:
            Optional expected base URL.

        request_type:
            Optional expected request type identifier.
    """
    assert captured.get("method") == method
    assert captured.get("path") == path
    if base_url is not None:
        assert captured.get("base_url") == base_url
    if request_type is not None:
        assert captured.get("request_type") == request_type
