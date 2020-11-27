import fastapi_plugins
from fastapi import FastAPI

from . import api
from .settings import config

app = FastAPI()
app.include_router(api.router, prefix=f"{config.API_PREFIX}/convert", tags=["currency"])


@app.on_event("startup")
async def on_startup() -> None:
    await fastapi_plugins.redis_plugin.init_app(app, config=config)
    await fastapi_plugins.redis_plugin.init()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await fastapi_plugins.redis_plugin.terminate()
