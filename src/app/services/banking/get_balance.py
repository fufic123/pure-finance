from typing import Callable
from uuid import UUID

from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.balance import Balance
from src.app.exceptions.account_not_found import AccountNotFound


class GetBalance:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, account_id: UUID, user_id: UUID) -> Balance | None:
        async with self._uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account is None or account.user_id != user_id:
                raise AccountNotFound()
            return await uow.balances.get_by_account(account_id)
