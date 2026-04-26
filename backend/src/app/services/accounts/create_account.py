from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.institution_not_found import InstitutionNotFound
from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.account import Account


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
        institution_id: UUID | None,
        name: str,
        currency: str,
        balance: Decimal,
    ) -> Account:
        now = self._clock.now()
        async with self._uow_factory() as uow:
            if institution_id is not None:
                institution = await uow.institutions.get_by_id(institution_id)
                if institution is None:
                    raise InstitutionNotFound()

            account = Account.create(
                user_id=user_id,
                iban=None,
                currency=currency,
                name=name,
                now=now,
                institution_id=institution_id,
                balance=balance,
            )
            await uow.accounts.add(account)
            return account
