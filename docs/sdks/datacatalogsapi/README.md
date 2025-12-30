# DataCatalogsAPI

## Overview

Endpoints for fetching data from Dateno registry of data catalogs.

Dateno catalog registry
<https://dateno.io/registry>

### Available Operations

* [get_catalog_by_id](#get_catalog_by_id) - Get Data Catalog Record
* [list_catalogs](#list_catalogs) - Search Data Catalogs

## get_catalog_by_id

This endpoint fetches a single item from the data catalog registry using its unique ID (UID). The full record will be returned. If the catalog has been merged into another catalog canonical entity, 
the request will automatically redirect to the new one.

   Check out the web version of the catalog registry: [Example catalog](https://dateno.io/registry/catalog/cdi00001616/).

### Example Usage

<!-- UsageSnippet language="python" operationID="get_catalog_by_id" method="get" path="/registry/catalog/{catalog_id}" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `catalog_id`                                                        | *str*                                                               | :heavy_check_mark:                                                  | UID of the data catalog to retrieve                                 | cdi00001616                                                         |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.DataCatalog](../../models/datacatalog.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## list_catalogs

Get a list of items from the data catalog.

Intro: [Dateno catalog registry](https://dateno.io/registry/).

### Example Usage

<!-- UsageSnippet language="python" operationID="list_catalogs" method="get" path="/registry/search/catalogs/" -->
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.list_catalogs(q="", limit=10, offset=0)

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `q`                                                                 | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `limit`                                                             | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `offset`                                                            | *Optional[int]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `software`                                                          | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `owner_type`                                                        | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `catalog_type`                                                      | *Optional[str]*                                                     | :heavy_minus_sign:                                                  | N/A                                                                 |
| `owner_country`                                                     | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `coverage_country`                                                  | List[*str*]                                                         | :heavy_minus_sign:                                                  | N/A                                                                 |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[models.DataCatalogSearchResponse](../../models/datacatalogsearchresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |