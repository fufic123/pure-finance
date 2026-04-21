from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.categorization_rule import CategorizationRuleModel
from src.domain.entities.categorization_rule import CategorizationRule


class PostgresCategorizationRuleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, rule: CategorizationRule) -> None:
        self._session.add(self._to_model(rule))

    async def get_by_id(self, rule_id: UUID) -> CategorizationRule | None:
        stmt = select(CategorizationRuleModel).where(CategorizationRuleModel.id == rule_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[CategorizationRule]:
        stmt = (
            select(CategorizationRuleModel)
            .where(CategorizationRuleModel.user_id == user_id)
            .order_by(CategorizationRuleModel.created_at)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def delete(self, rule_id: UUID) -> None:
        await self._session.execute(
            delete(CategorizationRuleModel).where(CategorizationRuleModel.id == rule_id)
        )

    @staticmethod
    def _to_entity(model: CategorizationRuleModel) -> CategorizationRule:
        return CategorizationRule(
            id=model.id,
            user_id=model.user_id,
            category_id=model.category_id,
            keyword=model.keyword,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: CategorizationRule) -> CategorizationRuleModel:
        return CategorizationRuleModel(
            id=entity.id,
            user_id=entity.user_id,
            category_id=entity.category_id,
            keyword=entity.keyword,
            created_at=entity.created_at,
        )
