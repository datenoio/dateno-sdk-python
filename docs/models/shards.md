# Shards

Shard stats from the ES response `_shards` section.


## Fields

| Field                | Type                 | Required             | Description          |
| -------------------- | -------------------- | -------------------- | -------------------- |
| `total`              | *int*                | :heavy_check_mark:   | N/A                  |
| `successful`         | *int*                | :heavy_check_mark:   | N/A                  |
| `skipped`            | *int*                | :heavy_check_mark:   | N/A                  |
| `failed`             | *int*                | :heavy_check_mark:   | N/A                  |
| `__pydantic_extra__` | Dict[str, *Any*]     | :heavy_minus_sign:   | N/A                  |