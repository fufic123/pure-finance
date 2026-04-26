from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.unit_of_work import UnitOfWork
from src.db.models.categorization_rule import CategorizationRule


class CreateRule:
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
        category_id: UUID,
        keyword: str,
    ) -> CategorizationRule:
        rule = CategorizationRule.create(
            user_id=user_id,
            category_id=category_id,
            keyword=keyword,
            now=self._clock.now(),
        )
        async with self._uow_factory() as uow:
            await uow.categorization_rules.add(rule)
        return rule
