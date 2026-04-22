from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.balance_snapshot import BalanceSnapshotModel
from src.domain.entities.balance_snapshot import BalanceSnapshot


class PostgresBalanceSnapshotRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, snapshot: BalanceSnapshot) -> None:
        self._session.add(self._to_model(snapshot))

    async def list_by_account(
        self,
        account_id: UUID,
        limit: int | None = None,
    ) -> list[BalanceSnapshot]:
        stmt = (
            select(BalanceSnapshotModel)
            .where(BalanceSnapshotModel.account_id == account_id)
            .order_by(BalanceSnapshotModel.recorded_at.desc())
        )
        if limit is not None:
            stmt = stmt.limit(limit)
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def latest(self, account_id: UUID) -> BalanceSnapshot | None:
        stmt = (
            select(BalanceSnapshotModel)
            .where(BalanceSnapshotModel.account_id == account_id)
            .order_by(BalanceSnapshotModel.recorded_at.desc())
            .limit(1)
        )
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: BalanceSnapshotModel) -> BalanceSnapshot:
        return BalanceSnapshot(
            id=model.id,
            account_id=model.account_id,
            amount=model.amount,
            recorded_at=model.recorded_at,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: BalanceSnapshot) -> BalanceSnapshotModel:
        return BalanceSnapshotModel(
            id=entity.id,
            account_id=entity.account_id,
            amount=entity.amount,
            recorded_at=entity.recorded_at,
            created_at=entity.created_at,
        )
