from datetime import datetime
from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.transaction import Transaction


class CreateTransaction:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    async def __call__(
        self,
        user_id: UUID,
        account_id: UUID,
        amount: Decimal,
        currency: str,
        description: str,
        booked_at: datetime,
        category_id: UUID | None,
        note: str | None,
    ) -> Transaction:
        async with self._uow_factory() as uow:
            account = await uow.accounts.get_by_id(account_id)
            if account is None or account.user_id != user_id:
                raise AccountNotFound()

            transaction = Transaction.create(
                account_id=account_id,
                amount=amount,
                currency=currency,
                description=description,
                booked_at=booked_at,
                now=self._clock.now(),
            )
            if note is not None:
                transaction.set_note(note)

            if category_id is not None:
                transaction.categorize(category_id, manually=True)
            else:
                rules = await uow.categorization_rules.list_by_user(user_id)
                for rule in rules:
                    if rule.matches(description):
                        transaction.categorize(rule.category_id, manually=False)
                        break

            await uow.transactions.add(transaction)
            return transaction
