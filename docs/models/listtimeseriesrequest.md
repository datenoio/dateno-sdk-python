# ListTimeseriesRequest


## Fields

| Field                                | Type                                 | Required                             | Description                          | Example                              |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ |
| `ns_id`                              | *str*                                | :heavy_check_mark:                   | Namespace identifier (database key). | ilostat                              |
| `start`                              | *Optional[int]*                      | :heavy_minus_sign:                   | Start offset (0-based).              | 0                                    |
| `limit`                              | *Optional[int]*                      | :heavy_minus_sign:                   | Maximum number of items to return.   | 100                                  |
| `apikey`                             | *OptionalNullable[str]*              | :heavy_minus_sign:                   | N/A                                  |                                      |