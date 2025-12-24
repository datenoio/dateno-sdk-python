# StatisticsAPI

## Overview

### Available Operations

* [list_namespaces_databases_statsdb_0_1_ns_get](#list_namespaces_databases_statsdb_0_1_ns_get) - List Namespaces / Databases
* [get_namespace_database_metadata_statsdb_0_1_ns_ns_id_get](#get_namespace_database_metadata_statsdb_0_1_ns_ns_id_get) - Get Namespace / Database Metadata
* [list_tables_statsdb_0_1_ns_ns_id_tables_get](#list_tables_statsdb_0_1_ns_ns_id_tables_get) - List Tables
* [get_table_metadata_statsdb_0_1_ns_ns_id_tables_table_id_get](#get_table_metadata_statsdb_0_1_ns_ns_id_tables_table_id_get) - Get Table Metadata
* [list_indicators_statsdb_0_1_ns_ns_id_indicators_get](#list_indicators_statsdb_0_1_ns_ns_id_indicators_get) - List Indicators
* [list_timeseries_statsdb_0_1_ns_ns_id_ts_get](#list_timeseries_statsdb_0_1_ns_ns_id_ts_get) - List Timeseries
* [get_indicator_metadata_statsdb_0_1_ns_ns_id_indicators_ind_id_get](#get_indicator_metadata_statsdb_0_1_ns_ns_id_indicators_ind_id_get) - Get Indicator Metadata
* [get_timeseries_record_metadata_statsdb_0_1_ns_ns_id_ts_ts_id_get](#get_timeseries_record_metadata_statsdb_0_1_ns_ns_id_ts_ts_id_get) - Get Timeseries Record Metadata
* [list_exportable_formats_statsdb_0_1_list_exportable_formats_get](#list_exportable_formats_statsdb_0_1_list_exportable_formats_get) - List Exportable Formats
* [export_timeseries_data_statsdb_0_1_ns_ns_id_ts_ts_id_export_fileext_get](#export_timeseries_data_statsdb_0_1_ns_ns_id_ts_ts_id_export_fileext_get) - Export Timeseries Data

## list_namespaces_databases_statsdb_0_1_ns_get

Return list of available namespaces / databases.

### Example Usage

<!-- UsageSnippet language="python" operationID="List_namespaces___databases_statsdb_0_1_ns_get" method="get" path="/statsdb/0.1/ns" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.list_namespaces_databases_statsdb_0_1_ns_get(start=0, limit=100)

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

## get_namespace_database_metadata_statsdb_0_1_ns_ns_id_get

Return namespace / database metadata (tables list).

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_namespace___database_metadata_statsdb_0_1_ns__ns_id__get" method="get" path="/statsdb/0.1/ns/{ns_id}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.get_namespace_database_metadata_statsdb_0_1_ns_ns_id_get(ns_id="ilostat")

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

## list_tables_statsdb_0_1_ns_ns_id_tables_get

Return list of available tables by namespace.

### Example Usage

<!-- UsageSnippet language="python" operationID="List_tables_statsdb_0_1_ns__ns_id__tables_get" method="get" path="/statsdb/0.1/ns/{ns_id}/tables" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.list_tables_statsdb_0_1_ns_ns_id_tables_get(ns_id="ilostat", start=0, limit=20)

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

## get_table_metadata_statsdb_0_1_ns_ns_id_tables_table_id_get

Get Table Metadata

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_table_metadata_statsdb_0_1_ns__ns_id__tables__table_id__get" method="get" path="/statsdb/0.1/ns/{ns_id}/tables/{table_id}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.get_table_metadata_statsdb_0_1_ns_ns_id_tables_table_id_get(ns_id="ilostat", table_id="CCF_XOXR_CUR_RT_A")

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

## list_indicators_statsdb_0_1_ns_ns_id_indicators_get

Return list of indicators metadata.

### Example Usage

<!-- UsageSnippet language="python" operationID="List_indicators_statsdb_0_1_ns__ns_id__indicators_get" method="get" path="/statsdb/0.1/ns/{ns_id}/indicators" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.list_indicators_statsdb_0_1_ns_ns_id_indicators_get(ns_id="ilostat", start=0, limit=100)

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

## list_timeseries_statsdb_0_1_ns_ns_id_ts_get

Return list of timeseries metadata.

### Example Usage

<!-- UsageSnippet language="python" operationID="List_timeseries_statsdb_0_1_ns__ns_id__ts_get" method="get" path="/statsdb/0.1/ns/{ns_id}/ts" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.list_timeseries_statsdb_0_1_ns_ns_id_ts_get(ns_id="ilostat", start=0, limit=100)

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

## get_indicator_metadata_statsdb_0_1_ns_ns_id_indicators_ind_id_get

Return indicator metadata (with optional metadata fields).

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_indicator_metadata_statsdb_0_1_ns__ns_id__indicators__ind_id__get" method="get" path="/statsdb/0.1/ns/{ns_id}/indicators/{ind_id}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.get_indicator_metadata_statsdb_0_1_ns_ns_id_indicators_ind_id_get(ns_id="ilostat", ind_id="WBL_XVET_SEX_EDU_NB")

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

## get_timeseries_record_metadata_statsdb_0_1_ns_ns_id_ts_ts_id_get

Get Timeseries Record Metadata

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_timeseries_record_metadata_statsdb_0_1_ns__ns_id__ts__ts_id__get" method="get" path="/statsdb/0.1/ns/{ns_id}/ts/{ts_id}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.get_timeseries_record_metadata_statsdb_0_1_ns_ns_id_ts_ts_id_get(ns_id="ilostat", ts_id="WBL_XVET_SEX_EDU_NB.CAN")

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

## list_exportable_formats_statsdb_0_1_list_exportable_formats_get

List exportable formats that could be used to export timeseries.

### Example Usage

<!-- UsageSnippet language="python" operationID="List_exportable_formats_statsdb_0_1_list_exportable_formats_get" method="get" path="/statsdb/0.1/list_exportable_formats" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.list_exportable_formats_statsdb_0_1_list_exportable_formats_get()

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

## export_timeseries_data_statsdb_0_1_ns_ns_id_ts_ts_id_export_fileext_get

Export data as file.

### Example Usage

<!-- UsageSnippet language="python" operationID="Export_timeseries_data_statsdb_0_1_ns__ns_id__ts__ts_id__export__fileext__get" method="get" path="/statsdb/0.1/ns/{ns_id}/ts/{ts_id}/export.{fileext}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.statistics_api.export_timeseries_data_statsdb_0_1_ns_ns_id_ts_ts_id_export_fileext_get(ns_id="ilostat", ts_id="WBL_XVET_SEX_EDU_NB.CAN", fileext="csv")

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

**[models.ExportTimeseriesDataStatsdb01NsNsIDTsTsIDExportFileextGetResponse](../../models/exporttimeseriesdatastatsdb01nsnsidtstsidexportfileextgetresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |