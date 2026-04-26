from datetime import datetime
from uuid import UUID

from src.db.models.refresh_token import RefreshToken


class InMemoryRefreshTokenRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, RefreshToken] = {}

    async def add(self, token: RefreshToken) -> None:
        self._by_id[token.id] = token

    async def update(self, token: RefreshToken) -> None:
        self._by_id[token.id] = token

    async def get_by_hash(self, token_hash: bytes) -> RefreshToken | None:
        for token in self._by_id.values():
            if token.token_hash == token_hash:
                return token
        return None

    async def revoke_all_for_user(self, user_id: UUID, now: datetime) -> None:
        for token in self._by_id.values():
            if token.user_id == user_id and not token.is_revoked:
                token.revoke(now)

    def __len__(self) -> int:
        return len(self._by_id)
