import pytest

MOCKED_CACHE_DATA = {
    "USD": 1.102193,
    "EUR": 1.303933,
    "PLN": 0.434111,
    "CZK": 3.222338,
    "timestamp": "2020-01-01T00:00:00+00:00",
}


@pytest.fixture()
async def mocked_redis():
    class MockedRedisFactory:
        @classmethod
        async def hgetall(cls, *args, **kwargs):
            return MOCKED_CACHE_DATA

    yield MockedRedisFactory
