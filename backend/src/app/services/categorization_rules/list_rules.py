from typing import Callable
from uuid import UUID

from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.categorization_rule import CategorizationRule


class ListRules:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, user_id: UUID) -> list[CategorizationRule]:
        async with self._uow_factory() as uow:
            return await uow.categorization_rules.list_by_user(user_id)
