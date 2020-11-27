from decimal import Decimal
from typing import Dict, Union

import fastapi_plugins
from aioredis import Redis
from fastapi import Depends


async def get(
    redis: Redis = Depends(fastapi_plugins.depends_redis),
) -> Dict[str, Union[Decimal, str]]:
    rates = await redis.hgetall("cache", encoding="utf=8")
    for currency in rates:
        if currency == "timestamp":
            continue
        rates[currency] = Decimal(rates[currency])
    return rates
