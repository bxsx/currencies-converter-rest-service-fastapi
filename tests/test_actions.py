from decimal import Decimal

import pytest

from app import actions, schemas
from app.settings import config


class TestActions:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "base,to,quote,timestamp",
        (
            ("USD", "EUR", 1.183035, "2020-01-01T00:00:00+00:00"),
            ("USD", "PLN", 0.393861, "2020-01-01T00:00:00+00:00"),
            ("USD", "CZK", 2.92357, "2020-01-01T00:00:00+00:00"),
            ("EUR", "USD", 0.845283, "2020-01-01T00:00:00+00:00"),
            ("EUR", "PLN", 0.332924, "2020-01-01T00:00:00+00:00"),
            ("EUR", "CZK", 2.471245, "2020-01-01T00:00:00+00:00"),
            ("PLN", "USD", 2.538966, "2020-01-01T00:00:00+00:00"),
            ("PLN", "EUR", 3.003686, "2020-01-01T00:00:00+00:00"),
            ("PLN", "CZK", 7.422843, "2020-01-01T00:00:00+00:00"),
            ("CZK", "USD", 0.342048, "2020-01-01T00:00:00+00:00"),
            ("CZK", "EUR", 0.404654, "2020-01-01T00:00:00+00:00"),
            ("CZK", "PLN", 0.134719, "2020-01-01T00:00:00+00:00"),
        ),
    )
    async def test_get_rate(self, base, to, quote, timestamp, mocked_cache_data):
        expected = schemas.ExchangeRate(quote=quote, timestamp=timestamp)

        actual = await actions.get_rate(
            schemas.SupportedCurrencyModel[base],
            schemas.SupportedCurrencyModel[to],
            rates=mocked_cache_data,
        )

        assert actual == expected

    @pytest.mark.asyncio
    async def test_get_rate_precision(self, mocked_cache_data):
        expected_precision = config.DECIMAL_PRECISION
        exchange_rate = await actions.get_rate(
            schemas.SupportedCurrencyModel["USD"],
            schemas.SupportedCurrencyModel["EUR"],
            rates=mocked_cache_data,
        )

        assert abs(exchange_rate.quote.as_tuple().exponent) == expected_precision

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "amount,quote,timestamp,expected",
        (
            (1, 1.0, "2020-01-01T00:00:00+00:00", 1.0),
            (1, 2.0, "2030-10-01T00:00:00+00:00", 2.0),
            (2, 1.0, "2020-01-01T00:00:00+00:00", 2.0),
            (2, 2.0, "2020-01-01T00:00:00+00:00", 4.0),
            (1.5, 2.0, "2020-01-01T20:45:10+00:00", 3.0),
            (1.1, 2.0, "2020-01-01T00:00:00+00:00", 2.2),
            (1.1, 0.1, "2030-10-01T00:00:00+00:00", 0.11),
            (10.5, 1.234, "1999-10-04T19:33:30+00:00", 12.957),
            (1.0, 0.1, "2023-05-01T00:00:00+00:00", 0.1),
            (1.123456, 1.0, "2020-03-24T00:00:00+00:00", 1.123456),
            (1.123456, 1.123456, "2020-11-22T16:33:11+10:00", 1.262153),
            (10.5, 100.1, "2022-02-02T22:22:22+00:00", 1051.05),
            (5.55, 1.11, "2021-08-30T00:00:01+00:00", 6.1605),
            (0.5, 0.000001, "2022-02-02T22:22:22+00:00", 0),
            (1000000, 1.23456789, "2020-01-01T00:00:00+00:00", 1234567.89),
            (0.000001, 0.000001, "2020-01-01T00:00:00+00:00", 0),
            (0.000009, 0.000001, "2021-08-31T00:00:01+00:00", 0),
            (0.000009, 0.1, "2021-08-31T00:00:01+00:00", 0.000001),
        ),
    )
    async def test_convert_currencies(self, amount, quote, timestamp, expected):
        mocked_get_rate = schemas.ExchangeRate(quote=quote, timestamp=timestamp)

        conversion = await actions.convert_currencies(
            Decimal(amount), exchange_rate=mocked_get_rate
        )

        assert conversion == round(Decimal(expected), 6)
