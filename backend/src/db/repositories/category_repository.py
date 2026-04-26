from uuid import UUID

from sqlalchemy import delete, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.category import Category


class PostgresCategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, category: Category) -> None:
        self._session.add(category)

    async def get_by_id(self, category_id: UUID) -> Category | None:
        result = await self._session.execute(select(Category).where(Category.id == category_id))
        return result.scalar_one_or_none()

    async def list_by_user(self, user_id: UUID) -> list[Category]:
        stmt = (
            select(Category)
            .where(or_(Category.user_id == user_id, Category.is_system.is_(True)))
            .order_by(Category.is_system.desc(), Category.name)
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def list_all(self) -> list[Category]:
        result = await self._session.execute(select(Category).order_by(Category.is_system.desc(), Category.name))
        return list(result.scalars().all())

    async def delete(self, category_id: UUID) -> None:
        await self._session.execute(delete(Category).where(Category.id == category_id))
