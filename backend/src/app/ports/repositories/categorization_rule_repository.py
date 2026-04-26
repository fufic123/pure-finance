from typing import Protocol
from uuid import UUID

from src.db.models.categorization_rule import CategorizationRule


class CategorizationRuleRepository(Protocol):
    async def add(self, rule: CategorizationRule) -> None: ...

    async def get_by_id(self, rule_id: UUID) -> CategorizationRule | None: ...

    async def list_by_user(self, user_id: UUID) -> list[CategorizationRule]: ...

    async def delete(self, rule_id: UUID) -> None: ...
