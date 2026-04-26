from uuid import UUID

from src.db.models.user import User
from src.app.exceptions.user_not_found import UserNotFound


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, User] = {}

    async def add(self, user: User) -> None:
        self._by_id[user.id] = user

    async def get_by_id(self, user_id: UUID) -> User:
        if user_id not in self._by_id:
            raise UserNotFound()
        return self._by_id[user_id]

    async def get_by_google_id(self, google_id: str) -> User | None:
        for user in self._by_id.values():
            if user.google_id == google_id:
                return user
        return None

    def __len__(self) -> int:
        return len(self._by_id)
