import fastapi_plugins
from pydantic import BaseSettings


class Settings(fastapi_plugins.RedisSettings, BaseSettings):
    API_PREFIX: str = "/api/currencies"
    DECIMAL_PRECISION: int = 6


config = Settings()
