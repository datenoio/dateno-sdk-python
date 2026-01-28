# dateno

Developer-friendly, type-safe Python SDK for working with the **Dateno API**.

This SDK provides a thin, well-typed client for accessing data catalogs, datasets,
search endpoints, and statistics exposed by the Datano platform.

> ⚠️ **Status**
>
> This SDK is intended primarily for **internal use, testing, and early integration**.
> The API surface may evolve between minor versions — pin versions explicitly.

---

## Table of Contents

- Overview
- Requirements
- Installation
- Authentication
- Quick Start
- Available APIs
- Error Handling
- Development
- License

---

## Overview

The Datano API allows you to:

- browse and search **data catalogs**
- retrieve **dataset metadata**
- perform **full-text and DSL-based search**
- work with **statistical namespaces, indicators, and time series**
- check service health

This SDK is a typed Python wrapper around those endpoints.

---

## Requirements

- Python **≥ 3.9**
- A valid **Dateno API key**

---

## Installation

### Install from GitHub

```bash
pip install "git+https://github.com/datenoio/dateno-sdk-python.git@v0.2.0"
```

### Local installation after cloning

```bash
git clone git@github.com:datenoio/dateno-sdk-python.git
cd dateno-sdk-python

python -m venv .venv
source .venv/bin/activate

pip install -e .
```

---

## Authentication

The SDK uses API key authentication via query parameter.

```python
SDK(api_key_query="YOUR_API_KEY")
```

---

## Quick Start

### Synchronous

```python
from dateno import SDK

with SDK(api_key_query="VhFBdk0NSod7RiYw2fwbcHYz7SZ3ye4u") as sdk:
    catalog = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")
    print(catalog)
```

### Asynchronous

```python
import asyncio
from dateno import SDK

async def main():
    async with SDK(api_key_query="VhFBdk0NSod7RiYw2fwbcHYz7SZ3ye4u") as sdk:
        catalog = await sdk.data_catalogs_api.get_catalog_by_id_async(catalog_id="cdi00001616")
        print(catalog)

#asyncio.run(main())
# В Jupyter:
await main()
```

---

## Available APIs

- Data Catalogs
- Search
- Raw Data Access
- Statistics
- Service

All responses are returned as **Pydantic models**.


---

## Search limits and pagination

The search endpoints support pagination via `limit` and `offset`.

⚠️ **Important limitation**

For dataset search requests (`search_datasets`), the Dateno API enforces a
**maximum `limit` of 500 items per request**.

If a value greater than `500` is provided, the server will **silently clamp**
the result size to `500`.

### Example: paginated dataset search

```python
from dateno import SDK

PAGE_SIZE = 500
offset = 0

with SDK(api_key_query="YOUR_API_KEY") as sdk:
    while True:
        resp = sdk.search_api.search_datasets(
            q="environment",
            limit=PAGE_SIZE,
            offset=offset,
        )

        hits = resp.hits.hits
        if not hits:
            break

        for hit in hits:
            print(hit.id, hit.source.dataset.title)

        offset += PAGE_SIZE
```
To retrieve large result sets, always use pagination with offset.

---

## Error Handling

```python
from dateno import SDK, errors

try:
    SDK(api_key_query="YOUR_API_KEY").service.get_healthz()
except errors.SDKError as e:
    print(e)
```

---

## Development

```bash
pytest
```

Integration tests:

```bash
DATENO_SERVER_URL=https://api.test.dateno.io DATENO_APIKEY=... pytest -m integration
```

---

## License

Apache License 2.0
