# SearchAPI

## Overview

Endpoints for searching datasets.

Dateno open search
<https://dateno.io/>

### Available Operations

* [get_single_dataset_record_by_entry_id_search_0_1_entry_entry_id_get](#get_single_dataset_record_by_entry_id_search_0_1_entry_entry_id_get) - Get Single Dataset Record By Entry Id
* [search_datasets_search_0_2_query_get](#search_datasets_search_0_2_query_get) - Search Datasets
* [dataset_search_using_elastic_dsl_search_0_2_es_search_post](#dataset_search_using_elastic_dsl_search_0_2_es_search_post) - Dataset Search Using Elastic Dsl
* [list_facets_search_0_2_list_facets_get](#list_facets_search_0_2_list_facets_get) - List Facets
* [get_facet_values_search_0_2_get_facet_get](#get_facet_values_search_0_2_get_facet_get) - Get Facet Values
* [get_similar_datasets_search_0_2_similar_entry_id_get](#get_similar_datasets_search_0_2_similar_entry_id_get) - Get Similar Datasets

## get_single_dataset_record_by_entry_id_search_0_1_entry_entry_id_get

Fetch information about one specific dataset (validated by Pydantic).

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_single_dataset_record_by_entry_id_search_0_1_entry__entry_id__get" method="get" path="/search/0.1/entry/{entry_id}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.search_api.get_single_dataset_record_by_entry_id_search_0_1_entry_entry_id_get(entry_id="c4a88574-7a2a-4048-bc9f-07de0559e7b7")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         | Example                                                             |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `entry_id`                                                          | *str*                                                               | :heavy_check_mark:                                                  | Dataset single record                                               | c4a88574-7a2a-4048-bc9f-07de0559e7b7                                |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |                                                                     |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |                                                                     |

### Response

**[models.SearchIndexEntry](../../models/searchindexentry.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 404                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500, 502, 503              | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## search_datasets_search_0_2_query_get

Search Datasets

### Example Usage

<!-- UsageSnippet language="python" operationID="Search_datasets_search_0_2_query_get" method="get" path="/search/0.2/query" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.search_api.search_datasets_search_0_2_query_get(q="Atlantic salmon", filters=[
        "\"source.catalog_type\"=\"Geoportal\"",
    ], limit=20, offset=0, facets=True, sort_by="_score")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                      | Type                                                                                                           | Required                                                                                                       | Description                                                                                                    | Example                                                                                                        |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `q`                                                                                                            | *Optional[str]*                                                                                                | :heavy_minus_sign:                                                                                             | Free-text search query, e.g. 'Atlantic salmon'                                                                 | Atlantic salmon                                                                                                |
| `filters`                                                                                                      | List[*str*]                                                                                                    | :heavy_minus_sign:                                                                                             | List of filters formatted as `"field"="value"` (quotes optional). Example: `"source.catalog_type"="Geoportal"` | "source.catalog_type"="Geoportal"                                                                              |
| `limit`                                                                                                        | *Optional[int]*                                                                                                | :heavy_minus_sign:                                                                                             | N/A                                                                                                            | 20                                                                                                             |
| `offset`                                                                                                       | *Optional[int]*                                                                                                | :heavy_minus_sign:                                                                                             | N/A                                                                                                            | 0                                                                                                              |
| `facets`                                                                                                       | *Optional[bool]*                                                                                               | :heavy_minus_sign:                                                                                             | If true, response includes aggregations/facets                                                                 | true                                                                                                           |
| `sort_by`                                                                                                      | *Optional[str]*                                                                                                | :heavy_minus_sign:                                                                                             | Comma-separated fields for sorting. Example: `_score` or `scores.feature_score`                                | _score                                                                                                         |
| `apikey`                                                                                                       | *OptionalNullable[str]*                                                                                        | :heavy_minus_sign:                                                                                             | N/A                                                                                                            |                                                                                                                |
| `retries`                                                                                                      | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                               | :heavy_minus_sign:                                                                                             | Configuration to override the default retry behavior of the client.                                            |                                                                                                                |

### Response

**[models.SearchQueryResponse](../../models/searchqueryresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500, 502, 503              | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## dataset_search_using_elastic_dsl_search_0_2_es_search_post

Dataset Search Using Elastic Dsl

### Example Usage

<!-- UsageSnippet language="python" operationID="Dataset_search_using_Elastic_DSL_search_0_2_es_search_post" method="post" path="/search/0.2/es_search" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.search_api.dataset_search_using_elastic_dsl_search_0_2_es_search_post(limit=20, offset=0, facets=True, sortby="_score", body={
        "query": {
            "match": {
                "title": "salmon",
            },
        },
        "post_filter": {
            "term": {
                "source.catalog_type": {
                    "value": "Geoportal",
                },
            },
        },
    })

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                                                                                                     | Type                                                                                                                                          | Required                                                                                                                                      | Description                                                                                                                                   | Example                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `limit`                                                                                                                                       | *Optional[int]*                                                                                                                               | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           | 20                                                                                                                                            |
| `offset`                                                                                                                                      | *Optional[int]*                                                                                                                               | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           | 0                                                                                                                                             |
| `facets`                                                                                                                                      | *Optional[bool]*                                                                                                                              | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           | true                                                                                                                                          |
| `sortby`                                                                                                                                      | *Optional[str]*                                                                                                                               | :heavy_minus_sign:                                                                                                                            | Comma-separated fields. Supported: _score, scores.feature_score                                                                               | _score                                                                                                                                        |
| `apikey`                                                                                                                                      | *OptionalNullable[str]*                                                                                                                       | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |                                                                                                                                               |
| `body`                                                                                                                                        | [Optional[models.BodyDatasetSearchUsingElasticDSLSearch02EsSearchPost]](../../models/bodydatasetsearchusingelasticdslsearch02essearchpost.md) | :heavy_minus_sign:                                                                                                                            | N/A                                                                                                                                           |                                                                                                                                               |
| `retries`                                                                                                                                     | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)                                                                              | :heavy_minus_sign:                                                                                                                            | Configuration to override the default retry behavior of the client.                                                                           |                                                                                                                                               |

### Response

**[models.SearchQueryResponse](../../models/searchqueryresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500, 502, 503              | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## list_facets_search_0_2_list_facets_get

Return list of facets available.

### Example Usage

<!-- UsageSnippet language="python" operationID="List_facets_search_0_2_list_facets_get" method="get" path="/search/0.2/list_facets" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.search_api.list_facets_search_0_2_list_facets_get()

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                           | Type                                                                | Required                                                            | Description                                                         |
| ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------- |
| `apikey`                                                            | *OptionalNullable[str]*                                             | :heavy_minus_sign:                                                  | N/A                                                                 |
| `retries`                                                           | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)    | :heavy_minus_sign:                                                  | Configuration to override the default retry behavior of the client. |

### Response

**[List[models.FacetInfo]](../../models/.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500                        | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## get_facet_values_search_0_2_get_facet_get

Returns values of a single facet:
- terms aggregation by `key`, size=5000
- no filters (empty bool.filter)
- response matches FacetValuesResponse: facet_key + items[key, num]

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_facet_values_search_0_2_get_facet_get" method="get" path="/search/0.2/get_facet" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.search_api.get_facet_values_search_0_2_get_facet_get(key="source.catalog_type")

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                            | Type                                                                 | Required                                                             | Description                                                          | Example                                                              |
| -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `key`                                                                | *Optional[str]*                                                      | :heavy_minus_sign:                                                   | Facet key from /search/0.2/list_facets (e.g. 'source.catalog_type'). | source.catalog_type                                                  |
| `apikey`                                                             | *OptionalNullable[str]*                                              | :heavy_minus_sign:                                                   | N/A                                                                  |                                                                      |
| `retries`                                                            | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)     | :heavy_minus_sign:                                                   | Configuration to override the default retry behavior of the client.  |                                                                      |

### Response

**[models.FacetValuesResponse](../../models/facetvaluesresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400                        | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500, 503                   | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |

## get_similar_datasets_search_0_2_similar_entry_id_get

Return a list of entries similar to the selected one.

### Example Usage

<!-- UsageSnippet language="python" operationID="Get_similar_datasets_search_0_2_similar__entry_id__get" method="get" path="/search/0.2/similar/{entry_id}" -->
```python
from dateno import SDK


with SDK() as sdk:

    res = sdk.search_api.get_similar_datasets_search_0_2_similar_entry_id_get(entry_id="c4a88574-7a2a-4048-bc9f-07de0559e7b7", limit=5, fields=[
        "dataset.title",
        "source.topics",
    ])

    # Handle response
    print(res)

```

### Parameters

| Parameter                                                              | Type                                                                   | Required                                                               | Description                                                            | Example                                                                |
| ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `entry_id`                                                             | *str*                                                                  | :heavy_check_mark:                                                     | Seed entry ID to search similar for                                    | c4a88574-7a2a-4048-bc9f-07de0559e7b7                                   |
| `limit`                                                                | *Optional[int]*                                                        | :heavy_minus_sign:                                                     | Number of results to return (1..100)                                   | 5                                                                      |
| `fields`                                                               | List[*str*]                                                            | :heavy_minus_sign:                                                     | Fields used for Elasticsearch more_like_this (repeatable query param). | [<br/>"dataset.title",<br/>"source.topics"<br/>]                       |
| `apikey`                                                               | *OptionalNullable[str]*                                                | :heavy_minus_sign:                                                     | N/A                                                                    |                                                                        |
| `retries`                                                              | [Optional[utils.RetryConfig]](../../models/utils/retryconfig.md)       | :heavy_minus_sign:                                                     | Configuration to override the default retry behavior of the client.    |                                                                        |

### Response

**[models.SimilarHitsResponse](../../models/similarhitsresponse.md)**

### Errors

| Error Type                 | Status Code                | Content Type               |
| -------------------------- | -------------------------- | -------------------------- |
| errors.ErrorResponse       | 400, 404                   | application/json           |
| errors.HTTPValidationError | 422                        | application/json           |
| errors.ErrorResponse       | 500, 503                   | application/json           |
| errors.SDKDefaultError     | 4XX, 5XX                   | \*/\*                      |