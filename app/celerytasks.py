from decimal import Decimal
from typing import Dict, List, Optional, Union

import requests
from celery import Celery
from pydantic import BaseSettings
from redis import Redis

from . import schemas


# Use separated settings for Celery to avoid installing unnecessary packages
class Settings(BaseSettings):
    # OpenExchange Rates
    OXR_ID: str
    OXR_URL: str

    # Celery settings
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int

    class Config:
        env_file = ".env"


class InvalidDataException(Exception):
    ...


config = Settings()
celery = Celery(
    "tasks", broker=config.CELERY_BROKER_URL, backend=config.CELERY_RESULT_BACKEND
)
celery.conf.timezone = "CET"


def _update_cache(rates: Dict[str, Union[Decimal, str]]) -> None:
    redis = Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=config.REDIS_DB)
    redis.hmset("cache", {k: str(rates[k]) for k in rates})


@celery.task(name="tasks.update_rates_via_openexchange")
def update_rates_via_openexchange(
    base: str = schemas.SupportedCurrencyModel.USD.value,
    currencies: Optional[List[schemas.SupportedCurrencyModel]] = None,
    api_id: Optional[str] = config.OXR_ID,
) -> Dict[str, Union[Decimal, str]]:
    if not api_id or api_id == "Missing API ID":
        raise InvalidDataException(config.OXR_ID)
    if currencies is None:
        currencies = [currency.value for currency in schemas.SupportedCurrencyModel]

    params = {"app_id": api_id, "symbols": ",".join(currencies), "base": base}
    response = requests.get(config.OXR_URL, params=params)

    if response.status_code != 200:
        raise InvalidDataException("OpenExchange response code", response.status_code)

    response_json = response.json()
    rates: Dict[str, Union[Decimal, str]] = {
        currency: Decimal(value) for currency, value in response_json["rates"].items()
    }
    rates["timestamp"] = response_json["timestamp"]

    _update_cache(rates)
    return rates
