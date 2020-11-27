import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app, config

client = TestClient(app)


class TestAPI:
    # TODO Add more test cases after adding the rates service. Mock in implementation for now.
    @pytest.mark.parametrize(
        "base,to,amount,rate,timestamp,expected",
        (
            ("USD", "EUR", 1, 1.164428, "2020-01-01T00:00:00+00:00", 1.164428),
            ("EUR", "PLN", 2, 1.164428, "2020-01-01T00:00:00+00:00", 2.328856),
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
