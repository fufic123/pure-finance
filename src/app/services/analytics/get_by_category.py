from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Callable
from uuid import UUID

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.ports.unit_of_work import UnitOfWork


@dataclass
class CategoryTotal:
    category_id: UUID | None
    total_eur: Decimal
    count: int


class GetAnalyticsByCategory:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(
        self,
        user_id: UUID,
        account_id: UUID | None = None,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[CategoryTotal]:
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

        totals: dict[UUID | None, list[Decimal]] = {}
        for t in transactions:
            if t.eur_amount is None:
                continue
            key = t.category_id
            if key not in totals:
                totals[key] = []
            totals[key].append(t.eur_amount)

        return [
            CategoryTotal(
                category_id=cat_id,
                total_eur=sum(amounts, Decimal("0")),
                count=len(amounts),
            )
            for cat_id, amounts in totals.items()
        ]
