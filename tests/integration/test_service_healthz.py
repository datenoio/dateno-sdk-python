import pytest


@pytest.mark.integration
def test_service_healthz(sdk):
    """
    Integration test for the `/healthz` service endpoint.

    This test verifies that the SDK-level `service.get_healthz()` call:
      - Successfully performs a real request against the configured server
      - Returns a response object that can be interpreted as structured data
      - Contains a top-level `status` field indicating service health

    The test is intentionally tolerant with respect to the response type,
    because the SDK may return:
      - A Pydantic model (preferred)
      - A plain dictionary
      - A lightweight object with attributes

    Only minimal, contract-level assertions are performed to ensure that:
      - The endpoint is reachable
      - The response schema has not regressed
      - The service reports a known health state

    Expected behavior:
      - `status` key MUST be present in the response payload
      - `status` value MUST be one of the documented states:
          * "ok"       — service is fully operational
          * "degraded" — service is available but partially impaired
    """
    # The method name is expected to match the smoke-test contract:
    # `service.get_healthz`
    res = sdk.service.get_healthz()

    # Normalize the response into a dictionary-like structure to keep
    # assertions robust against SDK internal representation changes.
    if hasattr(res, "model_dump"):
        payload = res.model_dump()
    elif isinstance(res, dict):
        payload = res
    else:
        payload = res.__dict__

    assert "status" in payload
    assert payload["status"] in ("ok", "degraded")
