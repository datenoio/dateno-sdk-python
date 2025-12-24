# SimilarHit

Single ES hit for similarity search.


## Fields

| Field                                                      | Type                                                       | Required                                                   | Description                                                |
| ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------- |
| `index`                                                    | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `id`                                                       | *str*                                                      | :heavy_check_mark:                                         | N/A                                                        |
| `score`                                                    | *OptionalNullable[float]*                                  | :heavy_minus_sign:                                         | Relevance score from Elasticsearch                         |
| `source`                                                   | Dict[str, *Any*]                                           | :heavy_check_mark:                                         | Document source (resources field removed for payload size) |