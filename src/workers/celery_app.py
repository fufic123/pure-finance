from celery import Celery

from src.shared.env import Settings
from src.shared.logging import configure_logging

configure_logging()

_settings = Settings()

celery_app = Celery(
    "pure_finance",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
    include=["src.workers.tasks.sync_all_transactions"],
)

celery_app.conf.beat_schedule = {
    "sync-transactions-every-6h": {
        "task": "src.workers.tasks.sync_all_transactions.sync_all_transactions",
        "schedule": 6 * 3600,
    },
}
celery_app.conf.timezone = "UTC"
