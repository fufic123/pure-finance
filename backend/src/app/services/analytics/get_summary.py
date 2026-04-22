from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.unit_of_work import UnitOfWork


@dataclass
class AnalyticsSummary:
    income: Decimal
    expenses: Decimal
    net: Decimal
    transaction_count: int


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
        for t in transactions:
            if t.amount >= 0:
                income += t.amount
            else:
                expenses += t.amount

        return AnalyticsSummary(
            income=income,
            expenses=expenses,
            net=income + expenses,
            transaction_count=len(transactions),
        )
