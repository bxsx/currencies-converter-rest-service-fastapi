import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app import actions, cache, schemas
from app.main import app
from app.settings import config

from .conftest import disable_patched_dep
from .helpers import supported_currencies

client = TestClient(app)


class TestAPI:
    @pytest.mark.parametrize(
        "base,to,amount,rate,timestamp,expected",
        (
            ("USD", "EUR", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("USD", "PLN", 1.5, 2.5, "2020-01-01T20:45:10+00:00", 3.75),
            ("USD", "CZK", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("EUR", "USD", 10, 2.225, "2030-10-01T00:00:00+00:00", 22.25),
            ("EUR", "PLN", 1.2, 1.234, "1999-10-04T19:33:30+00:00", 1.4808),
            ("EUR", "CZK", 3, 1.123456, "2023-05-01T00:00:00+00:00", 3.370368),
            ("PLN", "USD", 1.9, 2.0, "2020-03-24T00:00:00+00:00", 3.8),
            ("PLN", "EUR", 3.5, 2.5, "2020-11-22T16:33:11+10:00", 8.75),
            ("PLN", "CZK", 0.1, 2.0, "2021-02-01T11:00:00+00:00", 0.2),
            ("CZK", "USD", 0.5, 0.1, "2030-01-01T00:00:00+00:00", 0.05),
            ("CZK", "EUR", 10.5, 100.1, "2022-02-02T22:22:22+00:00", 1051.05),
            ("CZK", "PLN", 5.55, 1.11, "2021-08-30T00:00:01+00:00", 6.1605),
        ),
    )
    @disable_patched_dep(actions.get_rate)
    @disable_patched_dep(actions.convert_currencies)
    def test_convert_sut(self, base, to, amount, rate, timestamp, expected):
        expected_response = {
            "base": base,
            "to": to,
            "exchange_rate": {
                "quote": rate,
                "timestamp": timestamp,
            },
            "amount": amount,
            "result": expected,
        }
        app.dependency_overrides[actions.convert_currencies] = lambda: expected
        app.dependency_overrides[actions.get_rate] = lambda: schemas.ExchangeRate(
            quote=rate, timestamp=timestamp
        )

        response = client.get(f"{config.API_PREFIX}/convert/{base}/{to}/{amount}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "amount,rate,timestamp,expected",
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
    @pytest.mark.parametrize("base,to", supported_currencies.pair_iter())
    @disable_patched_dep(actions.get_rate)
    @disable_patched_dep(actions.convert_currencies)
    def test_convert_all_supported_currencies_with_mocked_rate(
        self, base, to, amount, rate, timestamp, expected
    ):
        expected_response = {
            "base": base,
            "to": to,
            "exchange_rate": {
                "quote": rate,
                "timestamp": timestamp,
            },
            "amount": amount,
            "result": expected,
        }
        app.dependency_overrides[actions.get_rate] = lambda: schemas.ExchangeRate(
            quote=rate, timestamp=timestamp
        )

        response = client.get(f"{config.API_PREFIX}/convert/{base}/{to}/{amount}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response

    @pytest.mark.parametrize(
        "amount,base_rate,to_rate,quote,timestamp,expected",
        (
            (1, 1.0, 1.0, 1.0, "2020-01-01T00:00:00+00:00", 1.0),
            (1, 1.0, 2.0, 2.0, "2030-10-01T00:00:00+00:00", 2.0),
            (1, 2.0, 0.25, 0.125, "2020-02-02T00:00:01+00:00", 0.125),
            (2, 0.5, 1.0, 2.0, "2020-01-01T00:00:00+00:00", 4.0),
            (2, 2.0, 1.0, 0.5, "2020-01-01T00:00:00+00:00", 1.0),
            (1.5, 2.0, 1.0, 0.5, "2020-01-01T20:45:10+00:00", 0.75),
            (1.1, 2.0, 3.1, 1.55, "2020-01-01T00:00:00+00:00", 1.705),
            (1.1, 0.1, 0.1, 1.0, "2030-10-01T00:00:00+00:00", 1.1),
            (10.5, 1.234, 3.5, 2.836305, "1999-10-04T19:33:30+00:00", 29.781202),
            (1.0, 0.5, 0.05, 0.1, "2023-05-01T00:00:00+00:00", 0.1),
            (1.123456, 0.1, 0.1, 1.0, "2020-03-24T00:00:00+00:00", 1.123456),
            (1.123456, 1.123456, 1.0, 0.890111, "2020-11-22T16:33:11+10:00", 1.000001),
            (10.5, 100.1, 0.5, 0.004995, "2022-02-02T22:22:22+00:00", 0.052448),
            (5.55, 1.11, 2.22, 2.0, "2021-08-30T00:00:01+00:00", 11.1),
            (0.5, 0.000001, 0.1, 100000, "2022-02-02T22:22:22+00:00", 50000),
            (0.000009, 0.1, 0.000001, 0.00001, "2021-08-31T00:00:01+00:00", 0),
            (0.000009, 10, 1, 0.1, "2021-08-31T00:00:01+00:00", 0.000001),
            (1, 0.5, 0.5, 1.0, "2020-01-01T00:00:00+00:00", 1.0),
            (10, 0.495730, 2.225, 4.488330, "2030-10-01T00:00:00+00:00", 44.8833),
        ),
    )
    @pytest.mark.parametrize("base,to", supported_currencies.pair_iter())
    @disable_patched_dep(actions.get_rate)
    @disable_patched_dep(actions.convert_currencies)
    def test_convert_all_supported_currencies_with_mocked_cache(
        self, base, to, amount, base_rate, to_rate, quote, timestamp, expected
    ):
        expected_response = {
            "base": base,
            "to": to,
            "exchange_rate": {
                "quote": quote,
                "timestamp": timestamp,
            },
            "amount": amount,
            "result": expected,
        }
        app.dependency_overrides[cache.get] = lambda: {
            base: base_rate,
            to: to_rate,
            "timestamp": timestamp,
        }

        response = client.get(f"{config.API_PREFIX}/convert/{base}/{to}/{amount}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
