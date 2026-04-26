import asyncio
import logging

from src.app.services.accounts.take_daily_snapshots import TakeDailySnapshots
from src.db.unit_of_work import SqlAlchemyUnitOfWork
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="tasks.take_daily_snapshots")
def take_daily_snapshots() -> None:
    async def _run() -> None:
        from src.db.session import create_engine, create_session_maker
        from src.integrations.clock import SystemClock
        from src.shared.env import Settings

        settings = Settings()
        engine = create_engine(settings.database_url)
        session_maker = create_session_maker(engine)

        def uow_factory():
            return SqlAlchemyUnitOfWork(session_maker)

        service = TakeDailySnapshots(uow_factory=uow_factory, clock=SystemClock())
        try:
            count = await service()
            logger.info("daily balance snapshots created", extra={"count": count})
        finally:
            await engine.dispose()

    asyncio.run(_run())
