from uuid import UUID

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.category import CategoryModel
from src.domain.entities.category import Category


class PostgresCategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, category: Category) -> None:
        self._session.add(self._to_model(category))

    async def get_by_id(self, category_id: UUID) -> Category | None:
        stmt = select(CategoryModel).where(CategoryModel.id == category_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[Category]:
        stmt = (
            select(CategoryModel)
            .where(or_(CategoryModel.user_id == user_id, CategoryModel.is_system.is_(True)))
            .order_by(CategoryModel.is_system.desc(), CategoryModel.name)
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def delete(self, category_id: UUID) -> None:
        await self._session.execute(
            delete(CategoryModel).where(CategoryModel.id == category_id)
        )

    @staticmethod
    def _to_entity(model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            user_id=model.user_id,
            parent_id=model.parent_id,
            name=model.name,
            is_system=model.is_system,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            user_id=entity.user_id,
            parent_id=entity.parent_id,
            name=entity.name,
            is_system=entity.is_system,
            created_at=entity.created_at,
        )
