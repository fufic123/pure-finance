from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.transaction import Transaction


class UpdateTransaction:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(
        self,
        transaction_id: UUID,
        user_id: UUID,
        *,
        note: str | None,
        note_provided: bool,
        category_id: UUID | None,
        category_provided: bool,
    ) -> Transaction:
        async with self._uow_factory() as uow:
            transaction = await uow.transactions.get_by_id(transaction_id)
            if transaction is None:
                raise TransactionNotFound()
            account = await uow.accounts.get_by_id(transaction.account_id)
            if account is None or account.user_id != user_id:
                raise TransactionNotFound()
            if note_provided:
                transaction.set_note(note)
            if category_provided:
                transaction.categorize(category_id, manually=True)
            await uow.transactions.update(transaction)
            return transaction
