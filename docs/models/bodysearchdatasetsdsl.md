# BodySearchDatasetsDsl


## Fields

| Field                                                           | Type                                                            | Required                                                        | Description                                                     | Example                                                         |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------- |
| `query`                                                         | Dict[str, *Any*]                                                | :heavy_minus_sign:                                              | Elastic DSL query object. If omitted, match_all is used.        | {<br/>"match": {<br/>"title": "salmon"<br/>}<br/>}              |
| `post_filter`                                                   | Dict[str, *Any*]                                                | :heavy_minus_sign:                                              | Facet filters as Elastic DSL post_filter (bool/term/etc).       | {<br/>"term": {<br/>"source.catalog_type": {<br/>"value": "Geoportal"<br/>}<br/>}<br/>} |