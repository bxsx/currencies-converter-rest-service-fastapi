from .. import supported_currencies as sc


def test_get_currency_iterator() -> None:
    iter(sc.currency_iter())


def test_get_limited_currency_iterator() -> None:
    maximum_value = len(list(sc.currency_iter()))

    for i in range(maximum_value):
        assert len(list(sc.currency_iter(limit=i))) == i
