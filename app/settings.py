import fastapi_plugins
from pydantic import BaseSettings


class Settings(fastapi_plugins.RedisSettings, BaseSettings):
    API_PREFIX: str = "/api/currencies"


config = Settings()
