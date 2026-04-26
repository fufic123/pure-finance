from datetime import date
from uuid import UUID

from src.db.models.transaction import Transaction


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, Transaction] = {}

    async def add(self, transaction: Transaction) -> None:
        self._by_id[transaction.id] = transaction

    async def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        return self._by_id.get(transaction_id)

    async def list_by_account(
        self,
        account_id: UUID,
        *,
        from_date: date | None = None,
        to_date: date | None = None,
        category_id: UUID | None = None,
    ) -> list[Transaction]:
        results = [t for t in self._by_id.values() if t.account_id == account_id]
        if from_date is not None:
            results = [t for t in results if t.booked_at.date() >= from_date]
        if to_date is not None:
            results = [t for t in results if t.booked_at.date() <= to_date]
        if category_id is not None:
            results = [t for t in results if t.category_id == category_id]
        return results

    async def list_by_accounts(
        self,
        account_ids: list[UUID],
        *,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Transaction]:
        results = [t for t in self._by_id.values() if t.account_id in account_ids]
        if from_date is not None:
            results = [t for t in results if t.booked_at.date() >= from_date]
        if to_date is not None:
            results = [t for t in results if t.booked_at.date() <= to_date]
        return results

    async def update(self, transaction: Transaction) -> None:
        self._by_id[transaction.id] = transaction

    async def delete(self, transaction_id: UUID) -> None:
        self._by_id.pop(transaction_id, None)
