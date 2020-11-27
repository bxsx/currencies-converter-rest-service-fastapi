from fastapi import FastAPI

from . import api
from .settings import config

app = FastAPI()
app.include_router(api.router, prefix=f"{config.API_PREFIX}/convert", tags=["currency"])
