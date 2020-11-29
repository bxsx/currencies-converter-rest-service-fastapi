import fastapi_plugins
from pydantic import BaseSettings


class Settings(fastapi_plugins.RedisSettings, BaseSettings):
    API_PREFIX: str
    DECIMAL_PRECISION: int

    class Config:
        env_file = ".env"


config = Settings()
