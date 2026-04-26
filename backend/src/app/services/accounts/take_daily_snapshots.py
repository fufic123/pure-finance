from typing import Callable

from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.balance_snapshot import BalanceSnapshot


class TakeDailySnapshots:
    def __init__(self, uow_factory: Callable[[], UnitOfWork], clock: Clock) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    async def __call__(self) -> int:
        now = self._clock.now()
        async with self._uow_factory() as uow:
            accounts = await uow.accounts.list_all()
            for account in accounts:
                snapshot = BalanceSnapshot.create(
                    account_id=account.id,
                    amount=account.balance,
                    recorded_at=now,
                    clock=self._clock,
                )
                await uow.balance_snapshots.add(snapshot)
            return len(accounts)
