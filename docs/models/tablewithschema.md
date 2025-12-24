# TableWithSchema

Extended table spec with schema details.


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              | Example                                                  |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `id`                                                     | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | forest17                                                 |
| `name`                                                   | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | Measurements                                             |
| `fields`                                                 | List[[models.FieldSpec](../models/fieldspec.md)]         | :heavy_minus_sign:                                       | N/A                                                      |                                                          |
| `ttype`                                                  | *Optional[str]*                                          | :heavy_minus_sign:                                       | N/A                                                      | [<br/>"data",<br/>"ref"<br/>]                            |
| `num_rows`                                               | *int*                                                    | :heavy_check_mark:                                       | N/A                                                      | 76998                                                    |
| `ind_key`                                                | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | indicator                                                |
| `dimensions`                                             | List[[models.DimensionSpec](../models/dimensionspec.md)] | :heavy_minus_sign:                                       | N/A                                                      |                                                          |
| `metadata`                                               | List[[models.MetadataField](../models/metadatafield.md)] | :heavy_minus_sign:                                       | N/A                                                      |                                                          |
| `schema_`                                                | List[[models.FieldSpec](../models/fieldspec.md)]         | :heavy_minus_sign:                                       | Detailed table schema                                    |                                                          |