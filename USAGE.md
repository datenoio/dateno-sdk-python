<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from dateno import SDK


with SDK() as sdk:

    res = sdk.data_catalogs_api.get_data_catalog_record_registry_catalog_catalog_id_get(catalog_id="cdi00001616")

    # Handle response
    print(res)
```

</br>

The same SDK client can also be used to make asynchronous requests by importing asyncio.

```python
# Asynchronous Example
import asyncio
from dateno import SDK

async def main():

    async with SDK() as sdk:

        res = await sdk.data_catalogs_api.get_data_catalog_record_registry_catalog_catalog_id_get_async(catalog_id="cdi00001616")

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->