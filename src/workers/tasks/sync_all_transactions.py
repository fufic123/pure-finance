import asyncio
import logging

from src.bootstrap import AppContainer
from src.shared.env import Settings
from src.workers.celery_app import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="src.workers.tasks.sync_all_transactions.sync_all_transactions")
def sync_all_transactions() -> None:
    asyncio.run(_sync())


async def _sync() -> None:
    container = AppContainer(Settings())
    try:
        sync = container.sync_transactions()
        sync_balance = container.sync_account_balance()

        async with container._uow_factory() as uow:
            accounts = await uow.accounts.list_all()

        for account in accounts:
            try:
                added = await sync(
                    account_id=account.id,
                    account_external_id=account.external_id,
                    user_id=account.user_id,
                )
                await sync_balance(account_id=account.id, account_external_id=account.external_id)
                logger.info("synced account %s: %d new transactions", account.id, added)
            except Exception:
                logger.exception("failed to sync account %s", account.id)
    finally:
        await container.dispose()
