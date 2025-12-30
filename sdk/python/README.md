# dateno

Developer-friendly & type-safe Python SDK specifically catered to leverage *dateno* API.

[![Built by Speakeasy](https://img.shields.io/badge/Built_by-SPEAKEASY-374151?style=for-the-badge&labelColor=f3f4f6)](https://www.speakeasy.com/?utm_source=dateno&utm_campaign=python)
[![License: MIT](https://img.shields.io/badge/LICENSE_//_MIT-3b5bdb?style=for-the-badge&labelColor=eff6ff)](https://opensource.org/licenses/MIT)


<br /><br />
> [!NOTE]
> This repository contains a pre-release Python SDK for internal testing.
> Install it from GitHub (see Installation section) and run `smoke_test.py` against a local or staging Datano API.

<!-- Start Summary [summary] -->
## Summary

The Datano API provides a set of endpoints for working with a registry of data catalogs and datasets.
It allows you to browse and search catalogs, retrieve dataset metadata, work with search indices and facets,
and access statistical namespaces, tables, indicators, and timeseries.

This Python SDK is a thin, typed client over the Datano API and is intended primarily for **internal testing
by data engineers and QA**.

### Authentication

All requests must include a valid API key passed as a **query parameter**.

Bearer authentication via request headers is **not supported** in this SDK.

Example:
```
https://api.dateno.io/[endpoint]?apikey=YOUR_API_KEY[other params]
```

The API key must be provided when initializing the SDK client via the `api_key_query` parameter.

For internal usage, API keys are issued by the Datano team.

<!-- Redoc-Inject: <security-definitions> -->
<!-- End Summary [summary] -->

<!-- Start Table of Contents [toc] -->
## Table of Contents
<!-- $toc-max-depth=2 -->
* [dateno](#dateno)
  * [Summary](#summary)
  * [Authentication](#authentication)
  * [Quick start (internal testing)](#quick-start-internal-testing)
  * [SDK Installation](#sdk-installation)
  * [IDE Support](#ide-support)
  * [SDK Example Usage](#sdk-example-usage)
  * [Smoke test](#smoke-test)
  * [Available Resources and Operations](#available-resources-and-operations)
  * [Retries](#retries)
  * [Error Handling](#error-handling)
  * [Server Selection](#server-selection)
  * [Custom HTTP Client](#custom-http-client)
  * [Resource Management](#resource-management)
  * [Debugging](#debugging)
* [Development](#development)
  * [Maturity](#maturity)
  * [Contributions](#contributions)

<!-- End Table of Contents [toc] -->

<!-- Start SDK Installation [installation] -->
## SDK Installation

This SDK is distributed **directly from GitHub** and is intended for internal testing.
Pin a specific tag to ensure reproducible environments.

> [!NOTE]
> **Python version policy**
>
> Once a Python version reaches its official end-of-life, a short grace period is provided
> for upgrades. After that, support for the EOL version may be removed.

The SDK can be installed using *uv*, *pip*, or *poetry*.

### uv

```bash
uv add git+https://github.com/datenoio/dateno-sdk-python.git@v0.1.0
```

### PIP

*PIP* is the default package installer for Python, enabling easy installation and management of packages from PyPI via the command line.

```bash
pip install "git+https://github.com/datenoio/dateno-sdk-python.git@v0.1.0"
```

For private repositories, SSH is recommended:

```bash
pip install "git+ssh://git@github.com/datenoio/dateno-sdk-python.git@v0.1.0"
```

### Poetry

*Poetry* is a modern tool that simplifies dependency management and package publishing by using a single `pyproject.toml` file to handle project metadata and dependencies.

```bash
poetry add git+https://github.com/datenoio/dateno-sdk-python.git@v0.1.0
```

### Local editable install (recommended for testing)
This is the preferred option for data engineers and QA when testing SDK changes:

```bash
git clone git@github.com:datenoio/dateno-sdk-python.git
cd dateno-sdk-python

python -m venv .venv
source .venv/bin/activate

pip install -e .
```
<!-- End SDK Installation [installation] -->

<!-- Start IDE Support [idesupport] -->
## IDE Support

### PyCharm

Generally, the SDK will work well with most IDEs out of the box. However, when using PyCharm, you can enjoy much better integration with Pydantic by installing an additional plugin.

- [PyCharm Pydantic Plugin](https://docs.pydantic.dev/latest/integrations/pycharm/)
<!-- End IDE Support [idesupport] -->

<!-- Start SDK Example Usage [usage] -->
## SDK Example Usage

### Example

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

<!-- Start Authentication [security] -->
## Authentication

### Per-Client Security Schemes

This SDK supports the following security scheme globally:

| Name            | Type   | Scheme  |
| --------------- | ------ | ------- |
| `api_key_query` | apiKey | API key |

To authenticate with the API the `api_key_query` parameter must be set when initializing the SDK client instance. For example:
```python
from dateno import SDK


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")

    # Handle response
    print(res)

```
<!-- End Authentication [security] -->

<!-- Start Available Resources and Operations [operations] -->
## Available Resources and Operations

<details open>
<summary>Available methods</summary>

### [DataCatalogsAPI](docs/sdks/datacatalogsapi/README.md)

* [get_catalog_by_id](docs/sdks/datacatalogsapi/README.md#get_catalog_by_id) - Get Data Catalog Record
* [list_catalogs](docs/sdks/datacatalogsapi/README.md#list_catalogs) - Search Data Catalogs

### [RawDataAccess](docs/sdks/rawdataaccess/README.md)

* [get_raw_entry_by_id](docs/sdks/rawdataaccess/README.md#get_raw_entry_by_id) - Get Raw Dataset Entry By Id

### [SearchAPI](docs/sdks/searchapi/README.md)

* [get_dataset_by_entry_id](docs/sdks/searchapi/README.md#get_dataset_by_entry_id) - Get Single Dataset Record By Entry Id
* [search_datasets](docs/sdks/searchapi/README.md#search_datasets) - Search Datasets
* [search_datasets_dsl](docs/sdks/searchapi/README.md#search_datasets_dsl) - Dataset Search Using Elastic Dsl
* [list_search_facets](docs/sdks/searchapi/README.md#list_search_facets) - List Facets
* [get_search_facet_values](docs/sdks/searchapi/README.md#get_search_facet_values) - Get Facet Values
* [get_similar_datasets](docs/sdks/searchapi/README.md#get_similar_datasets) - Get Similar Datasets

### [Service](docs/sdks/service/README.md)

* [get_healthz](docs/sdks/service/README.md#get_healthz) - Liveness probe

### [StatisticsAPI](docs/sdks/statisticsapi/README.md)

* [list_namespaces](docs/sdks/statisticsapi/README.md#list_namespaces) - List Namespaces / Databases
* [get_namespace](docs/sdks/statisticsapi/README.md#get_namespace) - Get Namespace / Database Metadata
* [list_namespace_tables](docs/sdks/statisticsapi/README.md#list_namespace_tables) - List Tables
* [get_namespace_table](docs/sdks/statisticsapi/README.md#get_namespace_table) - Get Table Metadata
* [list_indicators](docs/sdks/statisticsapi/README.md#list_indicators) - List Indicators
* [list_timeseries](docs/sdks/statisticsapi/README.md#list_timeseries) - List Timeseries
* [get_namespace_indicator](docs/sdks/statisticsapi/README.md#get_namespace_indicator) - Get Indicator Metadata
* [get_timeseries](docs/sdks/statisticsapi/README.md#get_timeseries) - Get Timeseries Record Metadata
* [list_export_formats](docs/sdks/statisticsapi/README.md#list_export_formats) - List Exportable Formats
* [export_timeseries_file](docs/sdks/statisticsapi/README.md#export_timeseries_file) - Export Timeseries Data

</details>
<!-- End Available Resources and Operations [operations] -->

<!-- Start Retries [retries] -->
## Retries

Some of the endpoints in this SDK support retries. If you use the SDK without any configuration, it will fall back to the default retry strategy provided by the API. However, the default retry strategy can be overridden on a per-operation basis, or across the entire SDK.

To change the default retry strategy for a single API call, simply provide a `RetryConfig` object to the call:
```python
from dateno import SDK
from dateno.utils import BackoffStrategy, RetryConfig


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616",
        RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False))

    # Handle response
    print(res)

```

If you'd like to override the default retry strategy for all operations that support retries, you can use the `retry_config` optional parameter when initializing the SDK:
```python
from dateno import SDK
from dateno.utils import BackoffStrategy, RetryConfig


with SDK(
    retry_config=RetryConfig("backoff", BackoffStrategy(1, 50, 1.1, 100), False),
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")

    # Handle response
    print(res)

```
<!-- End Retries [retries] -->

<!-- Start Error Handling [errors] -->
## Error Handling

[`SDKError`](./src/dateno/errors/sdkerror.py) is the base class for all HTTP error responses. It has the following properties:

| Property           | Type             | Description                                                                             |
| ------------------ | ---------------- | --------------------------------------------------------------------------------------- |
| `err.message`      | `str`            | Error message                                                                           |
| `err.status_code`  | `int`            | HTTP response status code eg `404`                                                      |
| `err.headers`      | `httpx.Headers`  | HTTP response headers                                                                   |
| `err.body`         | `str`            | HTTP body. Can be empty string if no body is returned.                                  |
| `err.raw_response` | `httpx.Response` | Raw HTTP response                                                                       |
| `err.data`         |                  | Optional. Some errors may contain structured data. [See Error Classes](#error-classes). |

### Example
```python
from dateno import SDK, errors


with SDK(
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:
    res = None
    try:

        res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")

        # Handle response
        print(res)


    except errors.SDKError as e:
        # The base class for HTTP error responses
        print(e.message)
        print(e.status_code)
        print(e.body)
        print(e.headers)
        print(e.raw_response)

        # Depending on the method different errors may be thrown
        if isinstance(e, errors.ErrorResponse):
            print(e.data.detail)  # str
```

### Error Classes
**Primary errors:**
* [`SDKError`](./src/dateno/errors/sdkerror.py): The base class for HTTP error responses.
  * [`ErrorResponse`](./src/dateno/errors/errorresponse.py): Standard error response payload. *
  * [`HTTPValidationError`](./src/dateno/errors/httpvalidationerror.py): Validation Error. Status code `422`. *

<details><summary>Less common errors (5)</summary>

<br />

**Network errors:**
* [`httpx.RequestError`](https://www.python-httpx.org/exceptions/#httpx.RequestError): Base class for request errors.
    * [`httpx.ConnectError`](https://www.python-httpx.org/exceptions/#httpx.ConnectError): HTTP client was unable to make a request to a server.
    * [`httpx.TimeoutException`](https://www.python-httpx.org/exceptions/#httpx.TimeoutException): HTTP request timed out.


**Inherit from [`SDKError`](./src/dateno/errors/sdkerror.py)**:
* [`ResponseValidationError`](./src/dateno/errors/responsevalidationerror.py): Type mismatch between the response data and the expected Pydantic model. Provides access to the Pydantic validation error via the `cause` attribute.

</details>

\* Check [the method documentation](#available-resources-and-operations) to see if the error is applicable.
<!-- End Error Handling [errors] -->

<!-- Start Server Selection [server] -->
## Server Selection

### Override Server URL Per-Client

The default server can be overridden globally by passing a URL to the `server_url: str` optional parameter when initializing the SDK client instance. For example:
```python
from dateno import SDK


with SDK(
    server_url="https://api.dateno.io",
    api_key_query="<YOUR_API_KEY_HERE>",
) as sdk:

    res = sdk.data_catalogs_api.get_catalog_by_id(catalog_id="cdi00001616")

    # Handle response
    print(res)

```
<!-- End Server Selection [server] -->

<!-- Start Custom HTTP Client [http-client] -->
## Custom HTTP Client

The Python SDK makes API calls using the [httpx](https://www.python-httpx.org/) HTTP library.  In order to provide a convenient way to configure timeouts, cookies, proxies, custom headers, and other low-level configuration, you can initialize the SDK client with your own HTTP client instance.
Depending on whether you are using the sync or async version of the SDK, you can pass an instance of `HttpClient` or `AsyncHttpClient` respectively, which are Protocol's ensuring that the client has the necessary methods to make API calls.
This allows you to wrap the client with your own custom logic, such as adding custom headers, logging, or error handling, or you can just pass an instance of `httpx.Client` or `httpx.AsyncClient` directly.

For example, you could specify a header for every request that this sdk makes as follows:
```python
from dateno import SDK
import httpx

http_client = httpx.Client(headers={"x-custom-header": "someValue"})
s = SDK(client=http_client)
```

or you could wrap the client with your own custom logic:
```python
from dateno import SDK
from dateno.httpclient import AsyncHttpClient
import httpx

class CustomClient(AsyncHttpClient):
    client: AsyncHttpClient

    def __init__(self, client: AsyncHttpClient):
        self.client = client

    async def send(
        self,
        request: httpx.Request,
        *,
        stream: bool = False,
        auth: Union[
            httpx._types.AuthTypes, httpx._client.UseClientDefault, None
        ] = httpx.USE_CLIENT_DEFAULT,
        follow_redirects: Union[
            bool, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
    ) -> httpx.Response:
        request.headers["Client-Level-Header"] = "added by client"

        return await self.client.send(
            request, stream=stream, auth=auth, follow_redirects=follow_redirects
        )

    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        content: Optional[httpx._types.RequestContent] = None,
        data: Optional[httpx._types.RequestData] = None,
        files: Optional[httpx._types.RequestFiles] = None,
        json: Optional[Any] = None,
        params: Optional[httpx._types.QueryParamTypes] = None,
        headers: Optional[httpx._types.HeaderTypes] = None,
        cookies: Optional[httpx._types.CookieTypes] = None,
        timeout: Union[
            httpx._types.TimeoutTypes, httpx._client.UseClientDefault
        ] = httpx.USE_CLIENT_DEFAULT,
        extensions: Optional[httpx._types.RequestExtensions] = None,
    ) -> httpx.Request:
        return self.client.build_request(
            method,
            url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
            extensions=extensions,
        )

s = SDK(async_client=CustomClient(httpx.AsyncClient()))
```
<!-- End Custom HTTP Client [http-client] -->

<!-- Start Resource Management [resource-management] -->
## Resource Management

The `SDK` class implements the context manager protocol and registers a finalizer function to close the underlying sync and async HTTPX clients it uses under the hood. This will close HTTP connections, release memory and free up other resources held by the SDK. In short-lived Python programs and notebooks that make a few SDK method calls, resource management may not be a concern. However, in longer-lived programs, it is beneficial to create a single SDK instance via a [context manager][context-manager] and reuse it across the application.

[context-manager]: https://docs.python.org/3/reference/datamodel.html#context-managers

```python
from dateno import SDK
def main():

    with SDK(
        api_key_query="<YOUR_API_KEY_HERE>",
    ) as sdk:
        # Rest of application here...


# Or when using async:
async def amain():

    async with SDK(
        api_key_query="<YOUR_API_KEY_HERE>",
    ) as sdk:
        # Rest of application here...
```
<!-- End Resource Management [resource-management] -->

<!-- Start Debugging [debug] -->
## Debugging

You can setup your SDK to emit debug logs for SDK requests and responses.

You can pass your own logger class directly into your SDK.
```python
from dateno import SDK
import logging

logging.basicConfig(level=logging.DEBUG)
s = SDK(debug_logger=logging.getLogger("dateno"))
```
<!-- End Debugging [debug] -->

<!-- Placeholder for Future Speakeasy SDK Sections -->

# Development

## Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

## Contributions

While we value open-source contributions to this SDK, this library is generated programmatically. Any manual changes added to internal files will be overwritten on the next generation. 
We look forward to hearing your feedback. Feel free to open a PR or an issue with a proof of concept and we'll do our best to include it in a future release. 

### SDK Created by [Speakeasy](https://www.speakeasy.com/?utm_source=dateno&utm_campaign=python)
