import pytest


@pytest.mark.integration
def test_statistics_indicator_get_wb_has_metadata(sdk):
    """
    Integration test for `statistics_api.get_namespace_indicator` ensuring metadata is present.

    This test performs a real request to the backend and verifies that a known indicator
    within the `wb` namespace includes a non-empty `metadata` field in the response.

    Why this test exists:
      - Historically, this specific indicator was verified via manual curl checks and was
        known to return metadata (e.g., `metadata_len` > 0).
      - Metadata handling is an area where backward/forward compatibility can regress
        (schema changes, generator changes, API fixes, etc.).
      - The test acts as a contract guard: for at least one stable indicator, metadata
        must be present and non-empty.

    Notes:
      - The SDK may represent `metadata` as `list[MetadataField]` (preferred strict typing)
        or a more permissive type depending on the current compatibility strategy.
      - We only assert presence and non-emptiness, not the exact schema of metadata items.

    Expected behavior:
      - The returned indicator object MUST expose the `metadata` attribute.
      - `metadata` MUST be non-empty (`len(metadata) > 0`).
    """
    # This indicator was previously verified manually (via curl) to include metadata.
    ind_id = "1.0.HCount.1.90usd"

    ind = sdk.statistics_api.get_namespace_indicator(ns_id="wb", ind_id=ind_id)

    md = getattr(ind, "metadata", None)

    # `metadata` is expected to be a list-like structure (ideally list[MetadataField]).
    assert md is not None
    assert len(md) > 0
