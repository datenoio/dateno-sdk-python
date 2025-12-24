# FacetValuesResponse

Facet values and counts for a given facet key.


## Fields

| Field                                            | Type                                             | Required                                         | Description                                      | Example                                          |
| ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ | ------------------------------------------------ |
| `facet_key`                                      | *str*                                            | :heavy_check_mark:                               | Facet field key                                  | source.catalog_type                              |
| `items`                                          | List[[models.FacetItem](../models/facetitem.md)] | :heavy_minus_sign:                               | Aggregated facet buckets                         |                                                  |