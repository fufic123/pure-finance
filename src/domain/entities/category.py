from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(slots=True)
class Category:
    id: UUID
    user_id: UUID | None  # None means system category
    parent_id: UUID | None
    name: str
    is_system: bool
    created_at: datetime

    @classmethod
    def create_user(
        cls,
        user_id: UUID,
        name: str,
        parent_id: UUID | None,
        now: datetime,
    ) -> "Category":
        return cls(
            id=uuid4(),
            user_id=user_id,
            parent_id=parent_id,
            name=name,
            is_system=False,
            created_at=now,
        )
