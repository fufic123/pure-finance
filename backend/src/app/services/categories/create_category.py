from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.category import Category


class CreateCategory:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock

    async def __call__(
        self,
        user_id: UUID,
        name: str,
        parent_id: UUID | None,
    ) -> Category:
        category = Category.create_user(
            user_id=user_id,
            name=name,
            parent_id=parent_id,
            now=self._clock.now(),
        )
        async with self._uow_factory() as uow:
            await uow.categories.add(category)
        return category
