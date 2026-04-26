from uuid import UUID

from pydantic import BaseModel

from src.db.models.categorization_rule import CategorizationRule


class RuleResponse(BaseModel):
    id: UUID
    category_id: UUID
    keyword: str

    @classmethod
    def from_rule(cls, rule: CategorizationRule) -> "RuleResponse":
        return cls(id=rule.id, category_id=rule.category_id, keyword=rule.keyword)
