import itertools
from typing import Generator, Optional, Tuple

from app.schemas import SupportedCurrencyModel


def currency_iter(
    limit: Optional[int] = None,
) -> Generator[SupportedCurrencyModel, None, None]:
    if limit is None:
        limit = len(SupportedCurrencyModel)

    return (c for c, _ in zip(SupportedCurrencyModel, range(limit)))


def pair_iter() -> Generator[
    Tuple[SupportedCurrencyModel, SupportedCurrencyModel], None, None
]:
    yield from itertools.permutations(list(SupportedCurrencyModel), 2)
