from decimal import Decimal
from functools import wraps

import pytest

from app import actions, schemas
from app.main import app


async def patch_action_get_rate():
    return schemas.ExchangeRate(quote=1.123456, timestamp="2020-01-01T00:00:00+00:00")


async def patch_action_convert_currencies():
    return Decimal(1.123456)


@pytest.fixture
async def patch_actions():
    copy = app.dependency_overrides.copy()
    app.dependency_overrides[actions.get_rate] = patch_action_get_rate
    app.dependency_overrides[
        actions.convert_currencies
    ] = patch_action_convert_currencies
    yield  # setup / teardown
    app.dependency_overrides = copy


def disable_patched_dep(dep):
    """
    Temporary disables already patched dependency for a decorated test case
    """

    def decorator(testcase):
        @wraps(testcase)
        def wrapper(*args, **kwargs):
            old = app.dependency_overrides.pop(dep, None)
            testcase(*args, **kwargs)
            if old:
                app.dependency_overrides[dep] = old
            else:
                app.dependency_overrides.pop(dep, None)

        return wrapper

    return decorator


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
