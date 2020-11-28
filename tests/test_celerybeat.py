from celery.schedules import crontab

from app.celerybeat import celery


class TestCeleryBeat:
    def test_should_run_everyday_at_3_30_am(self):
        assert celery.conf.beat_schedule["update-rates-everyday"][
            "schedule"
        ] == crontab(hour=3, minute=30)
