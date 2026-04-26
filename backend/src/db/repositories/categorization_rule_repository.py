from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.categorization_rule import CategorizationRule


class PostgresCategorizationRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, rule: CategorizationRule) -> None:
        self._session.add(rule)

    async def get_by_id(self, rule_id: UUID) -> CategorizationRule | None:
        result = await self._session.execute(select(CategorizationRule).where(CategorizationRule.id == rule_id))
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: UUID) -> list[CategorizationRule]:
        result = await self._session.execute(
            select(CategorizationRule).where(CategorizationRule.user_id == user_id).order_by(CategorizationRule.created_at)
        )
        return list(result.scalars().all())

    async def delete(self, rule_id: UUID) -> None:
        await self._session.execute(delete(CategorizationRule).where(CategorizationRule.id == rule_id))
