from uuid import UUID

from src.domain.entities.balance_snapshot import BalanceSnapshot


class InMemoryBalanceSnapshotRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, BalanceSnapshot] = {}

    async def add(self, snapshot: BalanceSnapshot) -> None:
        self._by_id[snapshot.id] = snapshot

    async def list_by_account(
        self,
        account_id: UUID,
        limit: int | None = None,
    ) -> list[BalanceSnapshot]:
        items = sorted(
            (s for s in self._by_id.values() if s.account_id == account_id),
            key=lambda s: s.recorded_at,
            reverse=True,
        )
        if limit is not None:
            items = items[:limit]
        return items

    async def latest(self, account_id: UUID) -> BalanceSnapshot | None:
        items = [s for s in self._by_id.values() if s.account_id == account_id]
        if not items:
            return None
        return max(items, key=lambda s: s.recorded_at)
