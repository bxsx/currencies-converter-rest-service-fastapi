import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.settings import config

client = TestClient(app)


class TestAPI:
    @pytest.mark.parametrize(
        "base,to,amount,rate,timestamp,expected",
        (
            ("USD", "EUR", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("EUR", "USD", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("USD", "PLN", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("PLN", "USD", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("PLN", "EUR", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("EUR", "PLN", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("CZK", "EUR", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
            ("EUR", "CZK", 1, 2.0, "2020-01-01T00:00:00+00:00", 2.0),
        ),
    )
    def test_convert(self, base, to, amount, rate, timestamp, expected):
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

        response = client.get(f"{config.API_PREFIX}/convert/{base}/{to}/{amount}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == expected_response
