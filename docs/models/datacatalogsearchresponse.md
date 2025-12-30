# DataCatalogSearchResponse

Search response for data catalogs.


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              | Example                                                                  |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `source`                                                                 | *Optional[Literal["api"]]*                                               | :heavy_minus_sign:                                                       | API version / source identifier                                          | api                                                                      |
| `meta`                                                                   | [models.SearchMeta](../models/searchmeta.md)                             | :heavy_check_mark:                                                       | Pagination metadata for list/search endpoints.                           |                                                                          |
| `data`                                                                   | List[[models.DataCatalogSearchItem](../models/datacatalogsearchitem.md)] | :heavy_minus_sign:                                                       | N/A                                                                      |                                                                          |