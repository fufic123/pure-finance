from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.db.models.user import User


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    @classmethod
    def from_user(cls, user: User) -> "UserResponse":
        return cls(id=user.id, email=user.email, created_at=user.created_at)
