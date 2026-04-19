from uuid import UUID

from src.domain.entities.categorization_rule import CategorizationRule


class InMemoryCategorizationRuleRepository:
    def __init__(self, rules: list[CategorizationRule] | None = None) -> None:
        self._by_id: dict[UUID, CategorizationRule] = {r.id: r for r in (rules or [])}

    async def add(self, rule: CategorizationRule) -> None:
        self._by_id[rule.id] = rule

    async def get_by_id(self, rule_id: UUID) -> CategorizationRule | None:
        return self._by_id.get(rule_id)

    async def list_by_user(self, user_id: UUID) -> list[CategorizationRule]:
        return [r for r in self._by_id.values() if r.user_id == user_id]

    async def delete(self, rule_id: UUID) -> None:
        self._by_id.pop(rule_id, None)
