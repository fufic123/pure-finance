import asyncio
import logging

from src.bootstrap import AppContainer
from src.shared.env import Settings
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.take_daily_snapshots")
def take_daily_snapshots() -> None:
    async def _run() -> None:
        container = AppContainer(Settings())
        try:
            count = await container.take_daily_snapshots()()
            logger.info("daily balance snapshots created", extra={"count": count})
        finally:
            await container.dispose()

    asyncio.run(_run())
