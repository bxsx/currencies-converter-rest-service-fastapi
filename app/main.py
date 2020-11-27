from fastapi import FastAPI

from . import api, settings

config = settings.Settings()

app = FastAPI()
app.include_router(api.router, prefix=f"{config.API_PREFIX}/convert", tags=["currency"])
