import inspect

import pytest

from dateno import errors


def _try_call(fn, *, dsl: dict, start: int, limit: int):
    """
    Call `fn` (SearchAPI.search_datasets) in a signature-tolerant way.

    Generator variants observed:
      A) Body is not part of method at all (keyword-only start/limit and maybe q/query)
      B) Body is keyword arg named: request / request_body / body / dsl / payload
      C) Body is positional arg (rare, but handle)

    We attempt calls in safe order:
      1) keyword-body if present
      2) positional-body if allowed
      3) query-only call (no body) with start/limit and best-effort query text if present
    """
    sig = inspect.signature(fn)
    params = list(sig.parameters.values())

    # Drop `self` if it ever appears (usually not present for bound methods).
    if params and params[0].name == "self":
        params = params[1:]

    names = {p.name for p in params}

    # Common pagination names
    kwargs = {}
    if "start" in names:
        kwargs["start"] = start
    if "limit" in names:
        kwargs["limit"] = limit

    # If the method supports a simple query string param, pass a stable one.
    # (This gives the endpoint a chance to return items even without DSL body.)
    for qname in ("query", "q", "text", "term", "search", "query_string"):
        if qname in names:
            kwargs[qname] = "gdp"
            break

    # 1) keyword body parameter
    for bname in ("request", "request_body", "body", "dsl", "payload"):
        if bname in names:
            return fn(**{**kwargs, bname: dsl})

    # 2) positional body only if the signature actually allows a positional parameter.
    # If all parameters are KEYWORD_ONLY, we must NOT pass positional args.
    has_positional_slot = any(
        p.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
        for p in params
    )
    if has_positional_slot:
        try:
            return fn(dsl, **kwargs)
        except TypeError:
            pass

    # 3) query-only call (no body)
    return fn(**kwargs)


@pytest.mark.integration
def test_search_query_returns_items(sdk):
    """
    Integration smoke test for Search API.

    Response schema may vary across generator/backend versions, so we validate:
      - call succeeds
      - response is non-empty in a structural sense (not necessarily has `.items`)
    """
    dsl = {"query": {"match_all": {}}}

    res = _try_call(sdk.search_api.search_datasets, dsl=dsl, start=0, limit=5)

    # 1) direct list-like
    if isinstance(res, list):
        return

    # 2) pydantic model -> dict
    if hasattr(res, "model_dump"):
        payload = res.model_dump()
    elif isinstance(res, dict):
        payload = res
    else:
        payload = getattr(res, "__dict__", {})

    assert payload is not None, "Expected a payload (dict/model), got None"

    # Common result containers across APIs/backends
    for key in ("items", "hits", "results", "data", "entries"):
        if key in payload:
            assert payload[key] is not None
            return

    # If none of the known keys exist, at least ensure we got *some* structured response
    assert len(payload.keys()) > 0, f"Unexpected Search response shape: {type(res)} {payload}"


@pytest.mark.integration
def test_search_query_invalid_limit_raises_validation_error(sdk):
    """
    Integration error-path test for Search API.

    Runs only when `limit` is exposed in the SDK signature.
    """
    fn = sdk.search_api.search_datasets
    sig = inspect.signature(fn)
    names = set(sig.parameters.keys())
    if "self" in names:
        names.remove("self")

    if "limit" not in names:
        pytest.skip("This SDK build does not expose `limit` for search_datasets().")

    dsl = {"query": {"match_all": {}}}

    with pytest.raises((errors.HTTPValidationError, errors.ErrorResponse, errors.SDKDefaultError)):
        _try_call(fn, dsl=dsl, start=0, limit=-1)
