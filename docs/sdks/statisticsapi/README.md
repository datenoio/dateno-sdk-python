# StatisticsAPI

## Overview

### Available Operations

* [list_namespaces](#list_namespaces) - List Namespaces / Databases
* [get_namespace](#get_namespace) - Get Namespace / Database Metadata
* [list_namespace_tables](#list_namespace_tables) - List Tables
* [get_namespace_table](#get_namespace_table) - Get Table Metadata
* [list_indicators](#list_indicators) - List Indicators
* [list_timeseries](#list_timeseries) - List Timeseries
* [get_namespace_indicator](#get_namespace_indicator) - Get Indicator Metadata
* [get_timeseries](#get_timeseries) - Get Timeseries Record Metadata
* [list_export_formats](#list_export_formats) - List Exportable Formats
* [export_timeseries_file](#export_timeseries_file) - Export Timeseries Data

## list_namespaces

Return list of available namespaces / databases.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_namespaces" method="get" path="/statsdb/0.1/ns" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.list_namespaces(start=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `start`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Pagination offset (0-based).                                        | 0                                                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of items to return.                                  | 100                                                                 |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.PageNamespace](../../models/pagenamespace.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## get_namespace

Return namespace / database metadata (tables list).

### Example Usage

<!-- UsageSnippet language="python" operationID="get_namespace" method="get" path="/statsdb/0.1/ns/{ns_id}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.get_namespace(ns_id="ilostat")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key).                                | ilostat                                                             |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.Namespace](../../models/namespace.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## list_namespace_tables

Return list of available tables by namespace.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_namespace_tables" method="get" path="/statsdb/0.1/ns/{ns_id}/tables" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.list_namespace_tables(ns_id="ilostat", start=0, limit=20)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key).                                | ilostat                                                             |
| `start`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Start offset for pagination.                                        | 0                                                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of items to return.                                  | 20                                                                  |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.PageTableListItem](../../models/pagetablelistitem.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## get_namespace_table

Get Table Metadata

### Example Usage

<!-- UsageSnippet language="python" operationID="get_namespace_table" method="get" path="/statsdb/0.1/ns/{ns_id}/tables/{table_id}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.get_namespace_table(ns_id="ilostat", table_id="CCF_XOXR_CUR_RT_A")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key).                                | ilostat                                                             |
| `table_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | Table identifier within the namespace.                              | CCF_XOXR_CUR_RT_A                                                   |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.TableWithSchema](../../models/tablewithschema.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## list_indicators

Return list of indicators metadata.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_indicators" method="get" path="/statsdb/0.1/ns/{ns_id}/indicators" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.list_indicators(ns_id="ilostat", start=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key).                                | ilostat                                                             |
| `start`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Start offset (0-based).                                             | 0                                                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of items to return.                                  | 100                                                                 |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.PageIndicator](../../models/pageindicator.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## list_timeseries

Return list of timeseries metadata.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_timeseries" method="get" path="/statsdb/0.1/ns/{ns_id}/ts" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.list_timeseries(ns_id="ilostat", start=0, limit=100)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key).                                | ilostat                                                             |
| `start`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Start offset (0-based).                                             | 0                                                                   |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | Maximum number of items to return.                                  | 100                                                                 |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.PageTimeseries](../../models/pagetimeseries.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## get_namespace_indicator

Return indicator metadata (with optional metadata fields).

### Example Usage

<!-- UsageSnippet language="python" operationID="get_namespace_indicator" method="get" path="/statsdb/0.1/ns/{ns_id}/indicators/{ind_id}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.get_namespace_indicator(ns_id="ilostat", ind_id="WBL_XVET_SEX_EDU_NB")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key).                                | ilostat                                                             |
| `ind_id`                                                            | *str*                                                               | :heavy_check_mark:                                                  | Indicator identifier to retrieve.                                   | WBL_XVET_SEX_EDU_NB                                                 |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.Indicator](../../models/indicator.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## get_timeseries

Get Timeseries Record Metadata

### Example Usage

<!-- UsageSnippet language="python" operationID="get_timeseries" method="get" path="/statsdb/0.1/ns/{ns_id}/ts/{ts_id}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.get_timeseries(ns_id="ilostat", ts_id="WBL_XVET_SEX_EDU_NB.CAN")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `ns_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Namespace identifier (database key)                                 | ilostat                                                             |
| `ts_id`                                                             | *str*                                                               | :heavy_check_mark:                                                  | Timeseries identifier to retrieve                                   | WBL_XVET_SEX_EDU_NB.CAN                                             |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.TimeseriesWithSchema](../../models/timeserieswithschema.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## list_export_formats

List exportable formats that could be used to export timeseries.

### Example Usage

<!-- UsageSnippet language="python" operationID="list_export_formats" method="get" path="/statsdb/0.1/list_exportable_formats" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.list_export_formats()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[Dict[str, str]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## export_timeseries_file

Export data as file.

### Example Usage

<!-- UsageSnippet language="python" operationID="export_timeseries_file" method="get" path="/statsdb/0.1/ns/{ns_id}/ts/{ts_id}/export.{fileext}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.statistics_api.export_timeseries_file(ns_id="ilostat", ts_id="WBL_XVET_SEX_EDU_NB.CAN", fileext="csv")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                    | Type                                                                         | Required                                                                     | Description                                                                  | Example                                                                      |
| ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| `ns_id`                                                                      | *str*                                                                        | :heavy_check_mark:                                                           | N/A                                                                          | ilostat                                                                      |
| `ts_id`                                                                      | *str*                                                                        | :heavy_check_mark:                                                           | Timeseries identifier to retrieve                                            | WBL_XVET_SEX_EDU_NB.CAN                                                      |
| `fileext`                                                                    | *str*                                                                        | :heavy_check_mark:                                                           | Data export extension (e.g. csv, xlsx, json). Unsupported values return 400. | csv                                                                          |
| `apikey`                                                                     | *OptionalNullable[str]*                                                      | :heavy_minus_sign:                                                           | N/A                                                                          |                                                                              |
| `retries`                                                                    | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)             | :heavy_minus_sign:                                                           | Configuration to override the default retry behavior of the client.          |                                                                              |

### Response

**[models.ExportTimeseriesFileResponse](../../models/exporttimeseriesfileresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |