from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel


class SupportedCurrencyModel(str, Enum):
    USD = "USD"
    EUR = "EUR"
    CZK = "CZK"
    PLN = "PLN"


class ExchangeRate(BaseModel):
    quote: Decimal
    timestamp: datetime


class ConvertModel(BaseModel):
    base: str
    to: str
    amount: Decimal
    exchange_rate: ExchangeRate
    result: Decimal

    class Config:
        schema_extra = {
            "example": {
                "base": "EUR",
                "to": "USD",
                "amount": 15.5,
                "exchange_rate": {
                    "quote": 1.164428,
                    "timestamp": "2020-01-01T00:00:00+00:00",
                },
                "result": 18.048634,
            }
        }
