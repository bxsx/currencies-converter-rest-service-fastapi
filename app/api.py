from decimal import Decimal
from typing import Any

from fastapi import APIRouter, Path

from . import schemas

router = APIRouter()


@router.get("/{base}/{to}/{amount}", response_model=schemas.ConvertModel)
async def convert(
    base: schemas.SupportedCurrencyModel = Path(
        ...,
        title="Base currency",
        description="Base currency for conversion",
    ),
    to: schemas.SupportedCurrencyModel = Path(
        ...,
        title="Target currency",
        description="Target currency for conversion",
    ),
    amount: Decimal = Path(
        ...,
        gt=0,
        title="Amount of money",
        description="Amount of money that going to be converted",
    ),
) -> Any:
    # TODO: Get exchange_rate from service
    quote = Decimal(1.164428)
    timestamp = "2020-01-01T00:00:00+00:00"
    result = amount * quote

    return {
        "base": base,
        "to": to,
        "amount": amount,
        "exchange_rate": {"quote": quote, "timestamp": timestamp},
        "result": result,
    }
