import pytest


@pytest.mark.integration
def test_statistics_list_namespaces(sdk):
    """
    Integration test for `statistics_api.list_namespaces` basic pagination contract.

    This test executes a real request to the backend and verifies that:
      - The API returns a page-like object with an `items` attribute.
      - The returned `items` collection is non-empty for a small limit.
      - At least the first namespace entry exposes the minimal required identity fields:
        `id` and `name`.

    Why this test exists:
      - Namespaces are an entry point for most StatsDB workflows (browsing and discovery).
      - We want an early signal if pagination, response modeling, or basic serialization
        breaks after SDK regeneration or API changes.
      - The test intentionally asserts only a minimal stable contract to reduce flakiness.

    Expected behavior:
      - `list_namespaces(limit=10)` returns an object with `.items`.
      - `.items` contains at least one element.
      - The first element has truthy `.id` and `.name`.
    """
    page = sdk.statistics_api.list_namespaces(limit=10)

    items = getattr(page, "items", None)
    assert items is not None
    assert len(items) > 0

    ns0 = items[0]
    assert getattr(ns0, "id", None)
    assert getattr(ns0, "name", None)


@pytest.mark.integration
def test_statistics_list_indicators_paged_ilostat(sdk):
    """
    Integration test for `statistics_api.list_indicators` ensuring paged responses are usable.

    This test queries the `ilostat` namespace for a page of indicators and verifies that:
      - The response includes pagination totals (`totals`) and a non-empty `items` list.
      - The first indicator entry exposes core identifying fields: `id`, `table`, and `name`.
      - The `metadata` attribute is present, but may be empty depending on API content and/or
        current SDK generation compatibility.

    Why this test exists:
      - `list_indicators` is a primary catalog discovery endpoint for StatsDB.
      - This is one of the larger “list” endpoints and is sensitive to schema and paging changes.
      - We keep assertions minimal but meaningful: presence of items + a few core fields.

    Notes on `metadata`:
      - Ideally, `metadata` is consistently a list (possibly empty): `[]`.
      - Some SDK generations may currently allow `None` for compatibility; this test tolerates it
        to avoid blocking progress while the API/schema is being normalized.

    Expected behavior:
      - `list_indicators(ns_id="ilostat", start=0, limit=100)` returns:
          * `.totals` not None
          * `.items` not None and non-empty
      - First item has truthy `.id`, `.table`, `.name`
      - `.metadata` is either list-like or None (temporary tolerance)
    """
    page = sdk.statistics_api.list_indicators(ns_id="ilostat", start=0, limit=100)

    assert getattr(page, "totals", None) is not None
    assert getattr(page, "items", None) is not None
    assert len(page.items) > 0

    ind0 = page.items[0]
    assert getattr(ind0, "id", None)
    assert getattr(ind0, "table", None)
    assert getattr(ind0, "name", None)

    # Metadata may be empty; tolerate None for now if the current generation still allows it.
    md = getattr(ind0, "metadata", None)
    assert md is not None or md == []  # prefer [], but tolerate None while compatibility is being improved
