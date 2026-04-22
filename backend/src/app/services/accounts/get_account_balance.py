from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.unit_of_work import UnitOfWork


@dataclass
class AccountBalance:
    amount: Decimal
    currency: str
    updated_at: datetime


class GetAccountBalance:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, account_id: UUID, user_id: UUID) -> AccountBalance | None:
        async with self._uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account is None or account.user_id != user_id:
                raise AccountNotFound()
            snapshot = await uow.balance_snapshots.latest(account_id)
            if snapshot is None:
                return None
            return AccountBalance(
                amount=snapshot.amount,
                currency=account.currency,
                updated_at=snapshot.recorded_at,
            )
