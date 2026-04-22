from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.account import Account
from src.domain.entities.balance_snapshot import BalanceSnapshot


class UpdateAccount:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    async def __call__(
        self,
        account_id: UUID,
        user_id: UUID,
        name: str | None,
        balance: Decimal | None,
        name_provided: bool,
        balance_provided: bool,
    ) -> Account:
        async with self._uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account is None or account.user_id != user_id:
                raise AccountNotFound()

            if name_provided and name is not None:
                account.rename(name)

            if balance_provided and balance is not None:
                account.apply_snapshot(balance)
                snapshot = BalanceSnapshot.create(
                    account_id=account.id,
                    amount=balance,
                    recorded_at=self._clock.now(),
                    clock=self._clock,
                )
                await uow.balance_snapshots.add(snapshot)

            await uow.accounts.update(account)
            return account
