import pytest

from app.schemas import SupportedCurrencyModel


class TestSchemas:
    @pytest.mark.parametrize("currency", ("USD", "EUR", "CZK", "PLN"))
    def test_should_support_currency(self, currency: str):
        assert hasattr(SupportedCurrencyModel, currency)
        assert getattr(SupportedCurrencyModel, currency) == currency
