from typing import Callable
from uuid import UUID

from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.category import Category


class ListCategories:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, user_id: UUID) -> list[Category]:
        async with self._uow_factory() as uow:
            return await uow.categories.list_by_user(user_id)
