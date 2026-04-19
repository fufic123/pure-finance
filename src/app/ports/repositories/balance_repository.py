from typing import Protocol
from uuid import UUID

from src.domain.entities.balance import Balance


class BalanceRepository(Protocol):
    async def upsert(self, balance: Balance) -> None: ...

    async def get_by_account(self, account_id: UUID) -> Balance | None: ...
