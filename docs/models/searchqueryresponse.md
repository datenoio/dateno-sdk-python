# SearchQueryResponse

Typed view of an Elasticsearch `_search` response.

What this model guarantees:
- Accepts both `aggregations` and `aggs` (via `AliasChoices`).
- Normalizes `hits.total` when ES returns a bare integer.
- Keeps ES-native field names through aliases and allows unknown fields to pass (`extra="allow"`).
- Applies light, non-destructive normalization to each hit's `_source`:
    * Ensures `_source.int_id` falls back to `_source.dataset.int_id` if missing.
    * Ensures `_source.resources` is always a list (empty if missing/null).
    * If `_source.dataset.num_resources` is missing, sets it to `len(_source.resources)`.
    * Unifies `source` / `sources`:
        - Preserves all sources in `_source.sources` (list).
        - Picks a primary one into `_source.source` (first with `is_primary=true`, otherwise the first).
        - Cleans each source's `subregions` by dropping items where both `id` and `name` are `null`.


## Fields

| Field                                                                    | Type                                                                     | Required                                                                 | Description                                                              |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| `took`                                                                   | *OptionalNullable[int]*                                                  | :heavy_minus_sign:                                                       | N/A                                                                      |
| `timed_out`                                                              | *OptionalNullable[bool]*                                                 | :heavy_minus_sign:                                                       | N/A                                                                      |
| `shards`                                                                 | [OptionalNullable[models.Shards]](../models/shards.md)                   | :heavy_minus_sign:                                                       | N/A                                                                      |
| `hits`                                                                   | [models.Hits](../models/hits.md)                                         | :heavy_check_mark:                                                       | The `hits` section with total, optional max_score, and the list of hits. |
| `aggregations`                                                           | Dict[str, *Any*]                                                         | :heavy_minus_sign:                                                       | N/A                                                                      |
| `__pydantic_extra__`                                                     | Dict[str, *Any*]                                                         | :heavy_minus_sign:                                                       | N/A                                                                      |