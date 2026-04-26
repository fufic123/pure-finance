from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.account import Account


class CreateAccount:
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
        name: str,
        currency: str,
        balance: Decimal,
    ) -> Account:
        now = self._clock.now()
        async with self._uow_factory() as uow:
            account = Account.create(
                user_id=user_id,
                iban=None,
                currency=currency,
                name=name,
                now=now,
                balance=balance,
            )
            await uow.accounts.add(account)
            return account
