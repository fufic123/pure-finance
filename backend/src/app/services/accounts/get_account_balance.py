from dataclasses import dataclass
from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.unit_of_work import UnitOfWork


@dataclass
class AccountBalance:
    amount: Decimal
    currency: str


class GetAccountBalance:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, account_id: UUID, user_id: UUID) -> AccountBalance:
        async with self._uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account is None or account.user_id != user_id:
                raise AccountNotFound()
            return AccountBalance(amount=account.balance, currency=account.currency)
