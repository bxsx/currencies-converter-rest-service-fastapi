from typing import Generator, Optional

from app.schemas import SupportedCurrencyModel


def currency_iter(limit: Optional[int] = None) -> Generator[str, None, None]:
    if limit is None:
        limit = len(SupportedCurrencyModel)

    return (c.value for c, _ in zip(SupportedCurrencyModel, range(limit)))
