from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.app_log import AppLog


class AppLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, log: AppLog) -> None:
        self._session.add(log)

    async def list_by_period(
        self,
        from_dt: datetime,
        to_dt: datetime,
        level: str | None = None,
        user_id: UUID | None = None,
    ) -> list[AppLog]:
        q = select(AppLog).where(AppLog.created_at >= from_dt, AppLog.created_at <= to_dt)
        if level is not None:
            q = q.where(AppLog.level == level)
        if user_id is not None:
            q = q.where(AppLog.user_id == user_id)
        q = q.order_by(AppLog.created_at.desc())
        result = await self._session.execute(q)
        return list(result.scalars().all())

    async def count_by_period(self, from_dt: datetime, to_dt: datetime, level: str | None = None) -> int:
        from sqlalchemy import func
        q = select(func.count()).select_from(AppLog).where(
            AppLog.created_at >= from_dt, AppLog.created_at <= to_dt
        )
        if level is not None:
            q = q.where(AppLog.level == level)
        result = await self._session.execute(q)
        return result.scalar_one()
