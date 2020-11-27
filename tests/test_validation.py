import pytest
from fastapi import status
from fastapi.testclient import TestClient

from app.main import app
from app.settings import config

from .helpers.supported_currencies import currency_iter

client = TestClient(app)
API_PREFIX = config.API_PREFIX
c1, c2 = list(currency_iter(limit=2))


class TestValidationError:
    @pytest.mark.parametrize(
        "amount",
        (
            0,
            -1,
            -1.0,
            -1.5,
            -2.0,
            -2.593,
            -39393.3932,
            "a",
            "aaa",
            "1234foobar",
            "foobar1234",
        ),
    )
    def test_amount_should_be_positive_number(self, amount):
        response = client.get(f"{API_PREFIX}/convert/{c1}/{c2}/{amount}")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("currency", currency_iter())
    def test_currency_name_has_three_characters_only(self, currency):
        response = client.get(f"{API_PREFIX}/convert/{c1}/{currency}/123")
        assert response.status_code == status.HTTP_200_OK

        response = client.get(f"{API_PREFIX}/convert/{currency}/{c1}/123")
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.parametrize("fake_currency", ("a", "ab", "abcd", "abcde", "abcdef"))
    def test_return_422_if_currency_name_has_not_three_characters(self, fake_currency):
        response = client.get(f"{API_PREFIX}/convert/{c1}/{fake_currency}/123")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        response = client.get(f"{API_PREFIX}/convert/{fake_currency}/{c1}/123")
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
