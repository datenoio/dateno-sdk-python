from __future__ import annotations

import pytest

from dateno.sdkconfiguration import SDKConfiguration, SERVERS
from dateno.types import UNSET


def _mk_cfg(**overrides) -> SDKConfiguration:
    """
    Build a minimal SDKConfiguration for unit tests.

    This helper constructs SDKConfiguration instances without real HTTP clients.
    Most tests only validate pure configuration logic and must not perform I/O.

    Args:
        **overrides:
            Field overrides to apply on top of a safe default configuration.

    Returns:
        SDKConfiguration: a configuration object suitable for unit testing.
    """
    base = dict(
        server_url="",
        server_idx=0,
        client=None,
        client_supplied=True,
        async_client=None,
        async_client_supplied=True,
        debug_logger=None,
        security=None,
        timeout_ms=None,
    )
    base.update(overrides)
    return SDKConfiguration(**base)


def test_retry_config_default_is_unset() -> None:
    """
    SDKConfiguration.retry_config must behave as "unset" by default.

    In the current SDK generation, SDKConfiguration is not a Pydantic BaseModel,
    so fields declared via `pydantic.Field(...)` may remain as `FieldInfo`
    on the constructed instance. In that case we validate the default factory.

    This test ensures the default preserves the OptionalNullable contract:
      - "not provided" => UNSET
    """
    cfg = _mk_cfg()

    rc = cfg.retry_config

    # If generation leaves a FieldInfo object on the instance, validate its default_factory().
    if hasattr(rc, "default_factory") and callable(getattr(rc, "default_factory", None)):
        assert rc.default_factory() is UNSET
    else:
        assert rc is UNSET


def test_get_server_details_prefers_server_url_override_and_strips_trailing_slash() -> None:
    """
    get_server_details() must prefer an explicit `server_url` override.

    When `server_url` is set and non-empty, it should be returned as the base URL,
    and any trailing slash must be removed (so URL joining stays predictable).
    """
    cfg = _mk_cfg(server_url="https://example.invalid/")
    base_url, headers = cfg.get_server_details()

    assert base_url == "https://example.invalid"
    assert headers == {}


def test_get_server_details_preserves_server_url_without_trailing_slash() -> None:
    """
    get_server_details() must return server_url verbatim when it has no trailing slash.

    This test exists to ensure remove_suffix only strips a single terminal '/' and does
    not introduce other modifications.
    """
    cfg = _mk_cfg(server_url="https://example.invalid")
    base_url, headers = cfg.get_server_details()

    assert base_url == "https://example.invalid"
    assert headers == {}


def test_get_server_details_falls_back_to_default_server_when_server_url_empty() -> None:
    """
    When server_url is empty, get_server_details() must fall back to SERVERS[server_idx].

    The SDK generator typically uses:
      - server_url="" (empty) as "no override"
      - server_idx=0 as default server selection
    """
    cfg = _mk_cfg(server_url="", server_idx=0)
    base_url, headers = cfg.get_server_details()

    assert base_url == SERVERS[0]
    assert headers == {}


def test_get_server_details_sets_server_idx_to_zero_when_none_and_server_url_missing() -> None:
    """
    When server_url is missing/None and server_idx is None, get_server_details() must:
      - set server_idx to 0
      - return SERVERS[0]

    This is a small but important behavior: the configuration object becomes consistent
    after the call, and downstream code can rely on `server_idx` being non-None.
    """
    cfg = _mk_cfg(server_url=None, server_idx=None)

    base_url, headers = cfg.get_server_details()

    assert cfg.server_idx == 0
    assert base_url == SERVERS[0]
    assert headers == {}


def test_get_server_details_raises_on_invalid_server_idx() -> None:
    """
    get_server_details() must raise IndexError for invalid server_idx.

    The SDK keeps the list of servers in `SERVERS`. Selecting outside the bounds
    should fail fast (Python's standard list indexing behavior).
    """
    cfg = _mk_cfg(server_url="", server_idx=999)

    with pytest.raises(IndexError):
        cfg.get_server_details()
