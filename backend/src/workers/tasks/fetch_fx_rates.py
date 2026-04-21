import asyncio
import logging

from src.bootstrap import AppContainer
from src.shared.env import Settings
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="src.workers.tasks.fetch_fx_rates.fetch_fx_rates")
def fetch_fx_rates() -> None:
    asyncio.run(_run())


async def _run() -> None:
    container = AppContainer(Settings())
    try:
        count = await container.fetch_fx_rates()()
        logger.info("fx_rates_fetched count=%d", count)
    finally:
        await container.dispose()
