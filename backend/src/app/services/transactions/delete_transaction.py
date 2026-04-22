from typing import Callable
from uuid import UUID

from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.app.ports.unit_of_work import UnitOfWork


class DeleteTransaction:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, transaction_id: UUID, user_id: UUID) -> None:
        async with self._uow_factory() as uow:
            transaction = await uow.transactions.get_by_id(transaction_id)
            if transaction is None:
                raise TransactionNotFound()
            account = await uow.accounts.get_by_id(transaction.account_id)
            if account is None or account.user_id != user_id:
                raise TransactionNotFound()
            await uow.transactions.delete(transaction_id)
