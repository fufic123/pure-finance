from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(slots=True)
class CategorizationRule:
    id: UUID
    user_id: UUID
    category_id: UUID
    keyword: str  # case-insensitive substring match against transaction description
    created_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        category_id: UUID,
        keyword: str,
        now: datetime,
    ) -> "CategorizationRule":
        return cls(
            id=uuid4(),
            user_id=user_id,
            category_id=category_id,
            keyword=keyword,
            created_at=now,
        )

    def matches(self, description: str) -> bool:
        return self.keyword.lower() in description.lower()
