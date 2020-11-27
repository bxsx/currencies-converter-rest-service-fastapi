from enum import Enum


class SupportedCurrencyModel(str, Enum):
    USD = "USD"
    EUR = "EUR"
    CZK = "CZK"
    PLN = "PLN"
