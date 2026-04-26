from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.account import Account


class UpdateAccount:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

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

            await uow.accounts.update(account)
            return account
