# ListNamespaceTablesRequest


## Fields

| Field                                | Type                                 | Required                             | Description                          | Example                              |
| ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ | ------------------------------------ |
| `ns_id`                              | *str*                                | :heavy_check_mark:                   | Namespace identifier (database key). | ilostat                              |
| `start`                              | *Optional[int]*                      | :heavy_minus_sign:                   | Start offset for pagination.         | 0                                    |
| `limit`                              | *Optional[int]*                      | :heavy_minus_sign:                   | Maximum number of items to return.   | 20                                   |
| `apikey`                             | *OptionalNullable[str]*              | :heavy_minus_sign:                   | N/A                                  |                                      |