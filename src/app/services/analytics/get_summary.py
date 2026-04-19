from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.unit_of_work import UnitOfWork


@dataclass
class AnalyticsSummary:
    income_eur: Decimal
    expenses_eur: Decimal
    net_eur: Decimal
    transaction_count: int
    transactions_without_fx: int


class GetAnalyticsSummary:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(
        self,
        user_id: UUID,
        account_id: UUID | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> AnalyticsSummary:
        async with self._uow_factory() as uow:
            if account_id is not None:
                account = await uow.accounts.get_by_id(account_id)
                if account is None or account.user_id != user_id:
                    raise AccountNotFound()
                account_ids = [account_id]
            else:
                accounts = await uow.accounts.list_by_user(user_id)
                account_ids = [a.id for a in accounts]

            transactions = await uow.transactions.list_by_accounts(
                account_ids,
                from_date=from_date,
                to_date=to_date,
            )

        income = Decimal("0")
        expenses = Decimal("0")
        without_fx = 0
        for t in transactions:
            if t.eur_amount is None:
                without_fx += 1
                continue
            if t.eur_amount >= 0:
                income += t.eur_amount
            else:
                expenses += t.eur_amount

        return AnalyticsSummary(
            income_eur=income,
            expenses_eur=expenses,
            net_eur=income + expenses,
            transaction_count=len(transactions),
            transactions_without_fx=without_fx,
        )
