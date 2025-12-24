# SimilarHitsResponse

Only the 'hits' section from ES response (legacy behavior).


## Fields

| Field                                              | Type                                               | Required                                           | Description                                        |
| -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- | -------------------------------------------------- |
| `total`                                            | [models.SimilarTotal](../models/similartotal.md)   | :heavy_check_mark:                                 | ES total hits object.                              |
| `max_score`                                        | *OptionalNullable[float]*                          | :heavy_minus_sign:                                 | N/A                                                |
| `hits`                                             | List[[models.SimilarHit](../models/similarhit.md)] | :heavy_minus_sign:                                 | N/A                                                |