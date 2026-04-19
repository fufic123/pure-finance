from uuid import UUID

from src.domain.entities.transaction import Transaction


class InMemoryTransactionRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, Transaction] = {}

    async def add(self, transaction: Transaction) -> None:
        self._by_id[transaction.id] = transaction

    async def get_by_external_id(self, external_id: str) -> Transaction | None:
        for t in self._by_id.values():
            if t.external_id == external_id:
                return t
        return None

    async def list_by_account(self, account_id: UUID) -> list[Transaction]:
        return [t for t in self._by_id.values() if t.account_id == account_id]
