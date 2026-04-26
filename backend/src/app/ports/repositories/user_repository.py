from typing import Protocol
from uuid import UUID

from src.db.models.user import User


class UserRepository(Protocol):
    async def add(self, user: User) -> None: ...

    async def get_by_id(self, user_id: UUID) -> User: ...

    async def get_by_google_id(self, google_id: str) -> User | None: ...
