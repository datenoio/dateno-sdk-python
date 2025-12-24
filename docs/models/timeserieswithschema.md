# TimeseriesWithSchema

Timeseries metadata with schema (and optional metadata).


## Fields

| Field                                                    | Type                                                     | Required                                                 | Description                                              | Example                                                  |
| -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- | -------------------------------------------------------- |
| `id`                                                     | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | WHOINT_MORT_200_AFR                                      |
| `indicator`                                              | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | MORT_200                                                 |
| `table`                                                  | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | MORT_200                                                 |
| `name`                                                   | *str*                                                    | :heavy_check_mark:                                       | N/A                                                      | Mortality - Africa                                       |
| `metadata`                                               | List[[models.MetadataField](../models/metadatafield.md)] | :heavy_minus_sign:                                       | N/A                                                      |                                                          |
| `schema_`                                                | List[[models.FieldSpec](../models/fieldspec.md)]         | :heavy_minus_sign:                                       | Schema for the underlying table                          |                                                          |