# tests/conftest.py
from __future__ import annotations

import os
import sys
from pathlib import Path
import asyncio
import logging

import pytest
import httpx

import dateno.sdk as sdk_mod
from dateno import SDK


# Ensure the tests directory is importable (works with pytest --import-mode=importlib)
TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))


def _env(name: str, default: str | None = None) -> str | None:
    v = os.getenv(name)
    return v if v not in (None, "") else default


# IMPORTANT:
# SDK uses weakref.finalize(self, close_clients, ...) where close_clients is imported in dateno.sdk.
# So we must patch dateno.sdk.close_clients BEFORE any SDK instance is created.
def _noop_close_clients(*args, **kwargs):
    return


sdk_mod.close_clients = _noop_close_clients


@pytest.fixture
def anyio_backend():
    # чтобы anyio не пытался trio
    return "asyncio"


@pytest.fixture(scope="session")
def dateno_server_url() -> str:
    # server_url для интеграции (если env не задан, берём дефолт тестового стенда)
    return _env("DATENO_SERVER_URL", "https://api.test.dateno.io")  # type: ignore[return-value]


@pytest.fixture(scope="session")
def dateno_apikey() -> str | None:
    """
    ВАЖНО: НЕ skip тут.
    Иначе unit-тесты будут скипаться просто потому что sdk() зависит от dateno_apikey.
    """
    return _env("DATENO_APIKEY")


def _close_async_client_best_effort(async_client: httpx.AsyncClient) -> None:
    """
    Закрыть AsyncClient так, чтобы не падать:
    - если лупа нет -> asyncio.run()
    - если луп есть -> create_task() (best effort)
    """
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        try:
            asyncio.run(async_client.aclose())
        except Exception:
            pass
    else:
        try:
            loop.create_task(async_client.aclose())
        except Exception:
            pass


@pytest.fixture
def sdk(
    request: pytest.FixtureRequest,
    dateno_server_url: str,
    dateno_apikey: str | None,
) -> SDK:
    """
    Один fixture для всех тестов:
    - unit: server_url=https://example.invalid, api_key_query=TEST_KEY
    - integration (маркер): server_url=DATENO_SERVER_URL, api_key_query=DATENO_APIKEY

    Маркер проверяем через request.node.keywords (это гарантированно есть).
    """
    is_integration = "integration" in request.node.keywords

    if is_integration and not dateno_apikey:
        pytest.skip("DATENO_APIKEY is not set; skipping integration tests.")

    server_url = dateno_server_url if is_integration else "https://example.invalid"
    api_key_query = dateno_apikey if is_integration else "TEST_KEY"

    sync_client = httpx.Client()
    async_client = httpx.AsyncClient()
    logger = logging.getLogger("dateno-sdk-tests")

    s = SDK(
        api_key_query=api_key_query,
        server_url=server_url,
        client=sync_client,
        async_client=async_client,
        debug_logger=logger,
    )

    try:
        yield s
    finally:
        # Мы передали клиенты сами -> закрываем сами.
        try:
            sync_client.close()
        except Exception:
            pass

        try:
            _close_async_client_best_effort(async_client)
        except Exception:
            pass

        # на всякий случай обнуляем ссылки
        s.sdk_configuration.client = None
        s.sdk_configuration.async_client = None
