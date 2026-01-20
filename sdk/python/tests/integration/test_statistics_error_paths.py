import pytest

from dateno import errors


@pytest.mark.integration
def test_statistics_get_namespace_unknown_raises(sdk):
    """
    Integration error-path test for Statistics API.

    Requesting a non-existent namespace should result in a typed SDK error.
    We don't enforce a single exception class because generator/API may differ;
    we enforce "must raise a known SDK error" instead of returning junk.
    """
    with pytest.raises((errors.ErrorResponse, errors.HTTPValidationError, errors.SDKDefaultError)):
        sdk.statistics_api.get_namespace(ns_id="__definitely_not_a_real_namespace__")


@pytest.mark.integration
def test_statistics_get_indicator_unknown_raises(sdk):
    """
    Integration error-path test for Statistics API.

    Requesting a non-existent indicator within a valid/invalid namespace should
    raise a typed SDK error.
    """
    with pytest.raises((errors.ErrorResponse, errors.HTTPValidationError, errors.SDKDefaultError)):
        sdk.statistics_api.get_namespace_indicator(
            ns_id="wb",
            ind_id="__definitely_not_a_real_indicator__",
        )
