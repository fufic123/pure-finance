from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.open_banking_provider import OpenBankingProvider
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.balance import Balance


class SyncAccountBalance:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        provider: OpenBankingProvider,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._provider = provider

    async def __call__(self, account_id: UUID, account_external_id: str) -> bool:
        info = await self._provider.get_balance(account_external_id)
        if info is None:
            return False
        balance = Balance(
            account_id=account_id,
            amount=info.amount,
            currency=info.currency,
            updated_at=self._clock.now(),
        )
        async with self._uow_factory() as uow:
            await uow.balances.upsert(balance)
        return True
