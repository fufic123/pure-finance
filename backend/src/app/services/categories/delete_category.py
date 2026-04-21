from typing import Callable
from uuid import UUID

from src.app.exceptions.cannot_delete_system_category import CannotDeleteSystemCategory
from src.app.exceptions.category_not_found import CategoryNotFound
from src.app.ports.unit_of_work import UnitOfWork


class DeleteCategory:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, category_id: UUID, user_id: UUID) -> None:
        async with self._uow_factory() as uow:
            category = await uow.categories.get_by_id(category_id)
            if category is None or (not category.is_system and category.user_id != user_id):
                raise CategoryNotFound()
            if category.is_system:
                raise CannotDeleteSystemCategory()
            await uow.categories.delete(category_id)
