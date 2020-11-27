from decimal import Decimal
from typing import Any, Dict

from fastapi import APIRouter, Depends, Path

from . import actions, schemas

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
    exchange_rate: schemas.ExchangeRate = Depends(actions.get_rate),
    result: Decimal = Depends(actions.convert_currencies),
) -> Dict[str, Any]:

    return {
        "base": base,
        "to": to,
        "amount": amount,
        "exchange_rate": exchange_rate,
        "result": result,
    }
