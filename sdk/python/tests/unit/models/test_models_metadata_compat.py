# tests/test_models_metadata_compat.py
from __future__ import annotations

import pytest

from dateno.models.namespace import Namespace
from dateno.models.indicator import Indicator


def test_namespace_accepts_object_metadata_if_any():
    """
    Validate that the Namespace model accepts arbitrary metadata objects.

    This test ensures compatibility with flexible metadata schemas coming
    from the API. In particular, it verifies that the `metadata` field:

      - Can accept a dictionary (object) instead of a strict list type
      - Does not fail validation when metadata structure is unknown or dynamic

    This behavior is required to:
      - Prevent breaking changes during SDK regeneration
      - Allow backend-side evolution of metadata without SDK updates

    The test is expected to:
      - FAIL if `metadata` is strictly typed (e.g. List[MetadataField])
      - PASS if `metadata` is typed as `Any` or an equivalent flexible type
    """
    payload = {
        "id": "wb",
        "name": "wb",
        "metadata": {"k": "v"},
    }

    namespace = Namespace.model_validate(payload)

    assert namespace.id == "wb"


def test_indicator_accepts_object_metadata_if_any():
    """
    Validate that the Indicator model accepts arbitrary metadata objects.

    This test mirrors the Namespace metadata compatibility check, but for
    the Indicator model. It confirms that:

      - The `metadata` field does not enforce a rigid schema
      - Object-like metadata (dict) is accepted during validation

    This is important because indicator metadata may vary significantly
    across datasets and providers, and strict typing would cause
    unnecessary validation failures.

    The test is expected to:
      - FAIL if `metadata` is strictly typed
      - PASS if `metadata` is flexible (e.g. Any)
    """
    payload = {
        "id": "X",
        "table": "X",
        "name": "X",
        "metadata": {"foo": "bar"},
    }

    indicator = Indicator.model_validate(payload)

    assert indicator.id == "X"
