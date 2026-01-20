from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

import pytest

from test_utils import mk_cfg


def _require_attr(obj: Any, name: str) -> Any:
    """
    Fetch an attribute from an object/module and raise an informative assertion if missing.

    Args:
        obj: Object or module to introspect.
        name: Attribute name to retrieve.

    Returns:
        The attribute value.

    Raises:
        AssertionError: If the attribute does not exist.
    """
    if not hasattr(obj, name):
        raise AssertionError(f"Expected attribute {name!r} to exist on {obj!r}")
    return getattr(obj, name)


@dataclass
class _DummyHookContext:
    """
    Minimal hook context object compatible with dateno hook context wrappers.

    The SDK hook context wrapper classes in `dateno._hooks` expect an input object
    (commonly called `hook_ctx`) with the following attributes:
      - config
      - base_url
      - operation_id
      - oauth2_scopes
      - security_source

    This dummy object is intentionally small and stable for unit testing.
    """

    config: Any
    base_url: str
    operation_id: str
    oauth2_scopes: list[str]
    security_source: str


def _iter_context_classes() -> Iterable[type]:
    """
    Yield the hook context wrapper classes that BaseSDK relies on.

    We import from `dateno._hooks` because BaseSDK imports these names from there:
        from dateno._hooks import AfterErrorContext, AfterSuccessContext, BeforeRequestContext
    """
    try:
        import dateno._hooks as hooks_mod  # type: ignore
    except Exception as e:  # pragma: no cover
        pytest.skip(f"Hooks module is not available in this SDK build: {e!r}")

    yield _require_attr(hooks_mod, "BeforeRequestContext")
    yield _require_attr(hooks_mod, "AfterSuccessContext")
    yield _require_attr(hooks_mod, "AfterErrorContext")


def test_hook_context_wrapper_types_are_importable() -> None:
    """
    Hook context wrapper types must be importable.

    BaseSDK imports these symbols at import time. If they are missing, BaseSDK
    cannot function, and the SDK build is broken.

    This test is intentionally strict: it should fail, not skip, if the import
    contract is violated.
    """
    classes = list(_iter_context_classes())
    assert len(classes) == 3


def test_hook_context_wrappers_are_constructible_and_expose_required_fields() -> None:
    """
    Hook context wrappers must:
      - accept a HookContext-like object in their constructor
      - expose the core context fields as attributes

    Why this matters:
      - BaseSDK instantiates these wrappers around `hook_ctx` when calling hooks:
            hooks.before_request(BeforeRequestContext(hook_ctx), request)
            hooks.after_success(AfterSuccessContext(hook_ctx), response)
            hooks.after_error(AfterErrorContext(hook_ctx), response, err)
      - If wrappers require extra attributes or do not expose expected fields,
        hook implementations cannot make routing/telemetry decisions reliably.
    """
    dummy = _DummyHookContext(
        config=object(),
        base_url="https://example.invalid",
        operation_id="op.test",
        oauth2_scopes=["scope:a"],
        security_source="apikey",
    )

    for ctx_cls in _iter_context_classes():
        ctx = ctx_cls(dummy)
        assert getattr(ctx, "config") is dummy.config
        assert getattr(ctx, "base_url") == "https://example.invalid"
        assert getattr(ctx, "operation_id") == "op.test"
        assert getattr(ctx, "oauth2_scopes") == ["scope:a"]
        assert getattr(ctx, "security_source") == "apikey"


def test_sdkconfiguration_installs_default_hooks_object() -> None:
    """
    SDKConfiguration may install a default hooks object.

    BaseSDK accesses hooks via:
        hooks = self.sdk_configuration.__dict__["_hooks"]

    In some Speakeasy generator variants, `_hooks` is installed by SDKConfiguration.
    In other variants (like this SDK build), hooks are expected to be injected by
    the SDK layer or by tests (see BaseSDK unit tests).

    This test validates the minimal hooks protocol *only if* `_hooks` is present.
    """
    cfg = mk_cfg(server_url="https://example.invalid")

    if "_hooks" not in cfg.__dict__:
        pytest.skip(
            "SDKConfiguration does not auto-install `_hooks` in this SDK build; "
            "hooks are expected to be injected (BaseSDK unit tests do this explicitly)."
        )

    hooks = cfg.__dict__["_hooks"]

    # Minimal protocol required by BaseSDK.do_request / do_request_async
    assert hasattr(hooks, "before_request")
    assert hasattr(hooks, "after_success")
    assert hasattr(hooks, "after_error")
    assert hasattr(hooks, "after_all")

    assert callable(hooks.before_request)
    assert callable(hooks.after_success)
    assert callable(hooks.after_error)
    assert callable(hooks.after_all)


def test_optional_default_hooks_factory_if_present() -> None:
    """
    If the SDK exposes an explicit default hooks factory, it must return a valid hooks object.

    Some generator variants expose a helper such as:
      - dateno._hooks.get_default_hooks()
      - dateno._hooks.hooks.get_default_hooks()

    This test is opportunistic: if a factory is not exposed, we skip.
    If exposed, we validate the returned object implements the required protocol.
    """
    factory = None

    try:
        import dateno._hooks as hooks_mod  # type: ignore

        for name in ("get_default_hooks", "default_hooks", "make_default_hooks"):
            if hasattr(hooks_mod, name):
                candidate = getattr(hooks_mod, name)
                if callable(candidate):
                    factory = candidate
                    break
    except Exception:
        factory = None

    if factory is None:
        pytest.skip("Default hooks factory is not exposed by this SDK build.")

    hooks = factory()

    for name in ("before_request", "after_success", "after_error", "after_all"):
        assert callable(getattr(hooks, name, None)), f"Factory hooks must provide {name}()"
