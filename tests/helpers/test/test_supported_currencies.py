import math

from app.schemas import SupportedCurrencyModel

from .. import supported_currencies as sc


def test_get_currency_iterator():
    iter(sc.currency_iter())


def test_get_limited_currency_iterator():
    maximum_value = len(list(sc.currency_iter()))

    for i in range(maximum_value):
        assert len(list(sc.currency_iter(limit=i))) == i


def test_iterate_over_currencies_pair():
    n = len(SupportedCurrencyModel)
    possible_combinations = math.perm(n, 2)

    returned_pairs = []
    for pair in sc.pair_iter():
        assert pair[0] in SupportedCurrencyModel
        assert pair[1] in SupportedCurrencyModel
        assert pair not in returned_pairs
        returned_pairs.append(pair)

    assert len(returned_pairs) == possible_combinations
