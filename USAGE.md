<!-- Start SDK Example Usage [usage] -->
```python
# Synchronous Example
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")

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

    async with SDK(
        api_key_query="<YOUR_API_KEY_HERE>",
    ) as sdk:

        res = await sdk.data_catalogs_api.get_catalog_by_id_async(catalog_id="cdi00001616")

        # Handle response
        print(res)

asyncio.run(main())
```
<!-- End SDK Example Usage [usage] -->