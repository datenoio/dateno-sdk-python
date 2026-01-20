import inspect
from typing import Any, Callable

import pytest

import dateno.errors as errors


def _call_search_datasets_dsl(
    fn: Callable[..., Any],
    dsl: dict,
    *,
    offset: int = 0,
    limit: int = 5,
) -> Any:
    """
    Call SearchAPI.search_datasets_dsl() in a signature-tolerant way.

    Generator variants may expose:
      - request body as: body / request / request_body / dsl / payload
      - pagination as: offset/limit (most likely), start/limit, from_/size
      - and may also expose no pagination (rare)

    We pass only the arguments that exist in the function signature.
    """
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    # For bound methods, "self" is usually already bound, but keep safe.
    if params and params[0].name == "self":
        params = params[1:]

    names = [p.name for p in params]
    kwargs: dict[str, Any] = {}

    # pagination mapping (best-effort)
    if "offset" in names:
        kwargs["offset"] = offset
    if "start" in names:
        kwargs["start"] = offset
    if "from_" in names:
        kwargs["from_"] = offset

    if "limit" in names:
        kwargs["limit"] = limit
    if "size" in names:
        kwargs["size"] = limit

    # body kw
    body_kw = None
    for candidate in ("body", "request", "request_body", "dsl", "payload"):
        if candidate in names:
            body_kw = candidate
            break

    # If body is supported as keyword
    if body_kw is not None:
        kwargs[body_kw] = dsl
        return fn(**kwargs)

    # Otherwise try positional body (if method expects at least one positional argument)
    positional_accepts = [
        p
        for p in params
        if p.kind
        in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]

    if positional_accepts:
        return fn(dsl, **kwargs)

    pytest.skip("This SDK build does not expose a request body for search_datasets_dsl().")


def _extract_any_results(res: Any) -> Any:
    """
    Extract any 'results-like' field from response.

    The ES search response can be:
      - dict-like
      - Pydantic model (model_dump)
      - custom object with __dict__
    """
    if isinstance(res, list):
        return res

    if hasattr(res, "model_dump"):
        payload = res.model_dump()
    elif isinstance(res, dict):
        payload = res
    else:
        payload = getattr(res, "__dict__", {})

    for key in ("hits", "items", "results", "data", "entries"):
        if isinstance(payload, dict) and key in payload:
            return payload[key]

    return payload


@pytest.mark.integration
def test_search_datasets_dsl_returns_response(sdk):
    """
    Integration smoke test for Search API: search_datasets_dsl (Elasticsearch DSL).
    """
    if not hasattr(sdk.search_api, "search_datasets_dsl"):
        pytest.skip("This SDK build does not expose SearchAPI.search_datasets_dsl().")

    dsl = {"query": {"match_all": {}}}

    res = _call_search_datasets_dsl(sdk.search_api.search_datasets_dsl, dsl, offset=0, limit=5)

    assert res is not None


@pytest.mark.integration
def test_search_datasets_dsl_invalid_limit_raises_typed_error_or_skips(sdk):
    """
    Error-path smoke test for search_datasets_dsl.

    If this SDK build doesn't expose any pagination argument we can invalidate,
    we skip. Otherwise pass negative limit/size and expect a typed SDK error.
    """
    if not hasattr(sdk.search_api, "search_datasets_dsl"):
        pytest.skip("This SDK build does not expose SearchAPI.search_datasets_dsl().")

    fn = sdk.search_api.search_datasets_dsl
    sig = inspect.signature(fn)
    names = list(sig.parameters.keys())
    if names and names[0] == "self":
        names = names[1:]

    limit_arg = None
    for candidate in ("limit", "size"):
        if candidate in names:
            limit_arg = candidate
            break
    if limit_arg is None:
        pytest.skip("This SDK build does not expose limit/size for search_datasets_dsl().")

    dsl = {"query": {"match_all": {}}}

    with pytest.raises((errors.HTTPValidationError, errors.ErrorResponse, errors.SDKDefaultError)):
        _call_search_datasets_dsl(fn, dsl, offset=0, limit=-1)
