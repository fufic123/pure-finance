from typing import Protocol
from uuid import UUID

from src.domain.entities.category import Category


class CategoryRepository(Protocol):
    async def add(self, category: Category) -> None: ...

    async def get_by_id(self, category_id: UUID) -> Category | None: ...

    async def list_by_user(self, user_id: UUID) -> list[Category]:
        """Returns system categories and user's own categories."""
        ...

    async def delete(self, category_id: UUID) -> None: ...
