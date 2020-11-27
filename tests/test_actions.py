import pytest

from app import actions, schemas
from app.settings import config


class TestActions:
    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "base,to,quote,timestamp",
        (
            (
                "EUR",
                "USD",
                0.845283,
                "2020-01-01T00:00:00+00:00",
            ),
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
