# RawDataAccess

## Overview

### Available Operations

* [get_raw_entry_by_id](#get_raw_entry_by_id) - Get Raw Dataset Entry By Id

## get_raw_entry_by_id

Retrieve a single dataset entry from the Elasticsearch index by its ID.

Returns:
- 404 if the document is not found
- 503 if search backend is unavailable

### Example Usage

<!-- UsageSnippet language="python" operationID="get_raw_entry_by_id" method="get" path="/raw/0.1/entry/{entry_id}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.raw_data_access.get_raw_entry_by_id(entry_id="c4a88574-7a2a-4048-bc9f-07de0559e7b7")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `entry_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | Search index single entry                                           | c4a88574-7a2a-4048-bc9f-07de0559e7b7                                |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.SearchIndexEntry](../../models/searchindexentry.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500, 503                   | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |