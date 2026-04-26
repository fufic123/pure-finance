from celery import Celery
from celery.schedules import crontab

from src.shared.env import Settings
from src.shared.logging import configure_logging

configure_logging()

_settings = Settings()

celery_app = Celery(
    "pure_finance",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
    include=["src.workers.tasks.balance_snapshots"],
)

celery_app.conf.timezone = "UTC"

celery_app.conf.beat_schedule = {
    "take-daily-snapshots": {
        "task": "tasks.take_daily_snapshots",
        "schedule": crontab(hour=23, minute=59),
    },
}
