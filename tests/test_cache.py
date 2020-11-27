import pytest

from app import cache

from .conftest import MOCKED_CACHE_DATA


class TestCache:
    @pytest.mark.asyncio
    @pytest.mark.parametrize("key,value", MOCKED_CACHE_DATA.items())
    async def test_get(self, key, value, mocked_redis):
        rates = await cache.get(redis=mocked_redis)

        assert rates[key] == value
