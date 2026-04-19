from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(slots=True)
class User:
    id: UUID
    google_id: str
    email: str
    created_at: datetime

    @classmethod
    def register(cls, google_id: str, email: str, now: datetime) -> "User":
        return cls(
            id=uuid4(),
            google_id=google_id,
            email=email,
            created_at=now,
        )
