from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.balance_snapshot import BalanceSnapshot


class PostgresBalanceSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, snapshot: BalanceSnapshot) -> None:
        self._session.add(snapshot)

    async def list_by_account(self, account_id: UUID, limit: int | None = None) -> list[BalanceSnapshot]:
        stmt = select(BalanceSnapshot).where(BalanceSnapshot.account_id == account_id).order_by(BalanceSnapshot.recorded_at.desc())
        if limit is not None:
            stmt = stmt.limit(limit)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def latest(self, account_id: UUID) -> BalanceSnapshot | None:
        result = await self._session.execute(
            select(BalanceSnapshot).where(BalanceSnapshot.account_id == account_id).order_by(BalanceSnapshot.recorded_at.desc()).limit(1)
        )
        return result.scalar_one_or_none()
