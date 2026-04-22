from celery import Celery

from src.shared.env import Settings
from src.shared.logging import configure_logging

configure_logging()

_settings = Settings()

celery_app = Celery(
    "pure_finance",
    broker=_settings.redis_url,
    backend=_settings.redis_url,
    include=[],
)

celery_app.conf.timezone = "UTC"
