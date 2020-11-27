from decimal import Decimal

import pytest

from app import actions, schemas
from app.main import app


async def patch_service_get_rate():
    return schemas.ExchangeRate(quote=2.0, timestamp="2020-01-01T00:00:00+00:00")


async def patch_service_convert_currencies():
    return Decimal(2.0)


app.dependency_overrides[actions.get_rate] = patch_service_get_rate
app.dependency_overrides[actions.convert_currencies] = patch_service_convert_currencies

MOCKED_CACHE_DATA = {
    "USD": 1.102193,
    "EUR": 1.303933,
    "PLN": 0.434111,
    "CZK": 3.222338,
    "timestamp": "2020-01-01T00:00:00+00:00",
}


@pytest.fixture(scope="function")
async def mocked_cache_data():
    yield MOCKED_CACHE_DATA


@pytest.fixture()
async def mocked_redis():
    class MockedRedisFactory:
        @classmethod
        async def hgetall(cls, *args, **kwargs):
            return MOCKED_CACHE_DATA

    yield MockedRedisFactory
