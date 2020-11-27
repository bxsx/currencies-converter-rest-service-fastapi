import pytest
import redis
import requests
from fastapi import status
from fastapi.encoders import jsonable_encoder

from app import celerytasks, schemas


class TestCeleryTasks:
    @pytest.mark.ext
    def test_update_rates__integration_test(self, mocker):
        mocker.patch("app.celerytasks._update_cache")
        rates = celerytasks.update_rates_via_openexchange()

        celerytasks._update_cache.assert_called_once_with(rates)
        for currency in schemas.SupportedCurrencyModel:
            assert currency.name in rates
        assert "timestamp" in rates

    def test_update_rates(self, mocker):
        class MockedResponse:
            status_code = status.HTTP_200_OK

            @classmethod
            def json(cls):
                rates = {
                    "disclaimer": "https://openexchangerates.org/terms/",
                    "license": "https://openexchangerates.org/license/",
                    "timestamp": 1449877801,
                    "base": "USD",
                    "rates": {
                        "USD": 1.102193,
                        "EUR": 1.303933,
                        "PLN": 0.434111,
                        "CZK": 3.222338,
                    },
                }
                return jsonable_encoder(rates)

        mocker.patch("app.celerytasks._update_cache")
        mocker.patch("requests.get")
        requests.get.return_value = MockedResponse

        rates = celerytasks.update_rates_via_openexchange()

        requests.get.assert_called_once()
        celerytasks._update_cache.assert_called_once_with(rates)
        for currency in schemas.SupportedCurrencyModel:
            assert currency.name in rates
        for currency, quote in MockedResponse.json()["rates"].items():
            assert rates[currency] == quote
        assert rates["timestamp"] == 1449877801

    def test_update_rates_wrong_response(self):
        with pytest.raises(celerytasks.InvalidDataException):
            celerytasks.update_rates_via_openexchange(base="foobar")

    def test_update_rates_missing_api_id(self):
        with pytest.raises(celerytasks.InvalidDataException):
            celerytasks.update_rates_via_openexchange(api_id="")

    def test_update_cache(self, mocker):
        mocker.patch("redis.Redis.hmset")
        celerytasks._update_cache({})
        redis.Redis.hmset.assert_called_once()
