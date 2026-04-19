from datetime import date
from typing import Protocol
from uuid import UUID

from src.domain.entities.transaction import Transaction


class TransactionRepository(Protocol):
    async def add(self, transaction: Transaction) -> None: ...

    async def get_by_external_id(self, external_id: str) -> Transaction | None: ...

    async def get_by_id(self, transaction_id: UUID) -> Transaction | None: ...

    async def list_by_account(
        self,
        account_id: UUID,
        *,
        from_date: date | None = None,
        to_date: date | None = None,
        category_id: UUID | None = None,
    ) -> list[Transaction]: ...

    async def update(self, transaction: Transaction) -> None: ...
