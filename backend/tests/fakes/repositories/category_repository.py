from uuid import UUID

from src.domain.entities.category import Category


class InMemoryCategoryRepository:
    def __init__(self, categories: list[Category] | None = None) -> None:
        self._by_id: dict[UUID, Category] = {c.id: c for c in (categories or [])}

    async def add(self, category: Category) -> None:
        self._by_id[category.id] = category

    async def get_by_id(self, category_id: UUID) -> Category | None:
        return self._by_id.get(category_id)

    async def list_by_user(self, user_id: UUID) -> list[Category]:
        return [
            c for c in self._by_id.values()
            if c.is_system or c.user_id == user_id
        ]

    async def delete(self, category_id: UUID) -> None:
        self._by_id.pop(category_id, None)
