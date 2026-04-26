from typing import Protocol
from uuid import UUID

from src.db.models.balance_snapshot import BalanceSnapshot


class BalanceSnapshotRepository(Protocol):
    async def add(self, snapshot: BalanceSnapshot) -> None: ...

    async def list_by_account(
        self,
        account_id: UUID,
        limit: int | None = None,
    ) -> list[BalanceSnapshot]: ...

    async def latest(self, account_id: UUID) -> BalanceSnapshot | None: ...
