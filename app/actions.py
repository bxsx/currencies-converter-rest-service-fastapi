from decimal import Decimal, localcontext
from typing import Any, Dict

from fastapi import Depends

from . import cache, schemas
from .settings import config


async def get_rate(
    base: schemas.SupportedCurrencyModel,
    to: schemas.SupportedCurrencyModel,
    rates: Dict[str, Any] = Depends(cache.get),
) -> schemas.ExchangeRate:
    with localcontext() as ctx:
        ctx.prec = 2 * config.DECIMAL_PRECISION
        current_rate = rates[to] / rates[base]
    current_rate = round(current_rate, config.DECIMAL_PRECISION)

    return schemas.ExchangeRate(quote=current_rate, timestamp=rates["timestamp"])


async def convert_currencies(
    amount: Decimal,
    exchange_rate: schemas.ExchangeRate = Depends(get_rate),
) -> Decimal:
    with localcontext() as ctx:
        ctx.prec = 2 * config.DECIMAL_PRECISION
        result = exchange_rate.quote * amount
    return round(result, config.DECIMAL_PRECISION)
