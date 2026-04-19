from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.open_banking_provider import OpenBankingProvider
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.transaction import Transaction


class SyncTransactions:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        provider: OpenBankingProvider,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._provider = provider

    async def __call__(self, account_id: UUID, account_external_id: str) -> int:
        infos = await self._provider.list_transactions(account_external_id)
        now = self._clock.now()
        added = 0

        async with self._uow_factory() as uow:
            for info in infos:
                existing = await uow.transactions.get_by_external_id(info.external_id)
                if existing is not None:
                    continue
                eur_amount = await self._to_eur(uow, info.currency, info.amount, info.booked_at.date())
                transaction = Transaction.create(
                    account_id=account_id,
                    external_id=info.external_id,
                    amount=info.amount,
                    currency=info.currency,
                    description=info.description,
                    booked_at=info.booked_at,
                    now=now,
                )
                transaction.eur_amount = eur_amount
                await uow.transactions.add(transaction)
                added += 1

        return added

    @staticmethod
    async def _to_eur(uow: UnitOfWork, currency: str, amount: Decimal, date) -> Decimal | None:
        if currency == "EUR":
            return amount
        rate = await uow.fx_rates.get_rate(currency, date)
        if rate is None:
            return None
        return (amount / rate).quantize(Decimal("0.0001"))
