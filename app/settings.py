from pydantic import BaseSettings


class Settings(BaseSettings):
    API_PREFIX: str = "/api/currencies"
