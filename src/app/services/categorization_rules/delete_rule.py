from typing import Callable
from uuid import UUID

from src.app.exceptions.rule_not_found import RuleNotFound
from src.app.ports.unit_of_work import UnitOfWork


class DeleteRule:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self, rule_id: UUID, user_id: UUID) -> None:
        async with self._uow_factory() as uow:
            rule = await uow.categorization_rules.get_by_id(rule_id)
            if rule is None or rule.user_id != user_id:
                raise RuleNotFound()
            await uow.categorization_rules.delete(rule_id)
