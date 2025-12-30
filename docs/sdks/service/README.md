# Service

## Overview

### Available Operations

* [get_healthz](#get_healthz) - Liveness probe

## get_healthz

Health check endpoint.

Performs shallow checks for backend dependencies:

- **Elasticsearch**: `ping()` call.
- **MongoDB**: `admin.command("ping")`.
- **DuckDB**: only verifies that a connection object exists (no I/O).

Returns `200 OK` with a status payload if every dependency is reachable.
Returns `503 Service Unavailable` with a detailed payload if any check fails.
Always includes the application version from settings.

### Example Usage

<!-- UsageSnippet language="python" operationID="get_healthz" method="get" path="/healthz" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.service.get_healthz()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Dict[str, Any]](../../models/.md)**

### Errors

| Error Type             | Status Code            | Content Type           |
| ---------------------- | ---------------------- | ---------------------- |
| errors.SDKDefaultError | 4XX, 5XX               | \*/\*                  |