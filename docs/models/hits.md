# Hits

The `hits` section with total, optional max_score, and the list of hits.


## Fields

| Field                                        | Type                                         | Required                                     | Description                                  |
| -------------------------------------------- | -------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| `total`                                      | [models.TotalUnion](../models/totalunion.md) | :heavy_check_mark:                           | N/A                                          |
| `max_score`                                  | *OptionalNullable[float]*                    | :heavy_minus_sign:                           | N/A                                          |
| `hits`                                       | List[[models.Hit](../models/hit.md)]         | :heavy_check_mark:                           | N/A                                          |
| `__pydantic_extra__`                         | Dict[str, *Any*]                             | :heavy_minus_sign:                           | N/A                                          |