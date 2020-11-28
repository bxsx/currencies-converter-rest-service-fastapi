from celery import Celery
from celery.schedules import crontab
from pydantic import BaseSettings

from . import celerytasks


# Use separated settings for Celery to avoid installing unnecessary packages
class Settings(BaseSettings):
    # Celery settings
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    class Config:
        env_file = ".env"


config = Settings()
celery = Celery(
    "tasks", broker=config.CELERY_BROKER_URL, backend=config.CELERY_RESULT_BACKEND
)
celery.conf.timezone = "CET"

celery.conf.beat_schedule = {
    "update-rates-everyday": {
        "task": "tasks.update_rates_via_openexchange",
        "schedule": crontab(hour=3, minute=30),
    }
}

# Run a task on startup of heartbeat and fill in cache
celerytasks.update_rates_via_openexchange.apply_async()
