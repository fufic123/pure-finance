from datetime import datetime
from typing import Protocol
from uuid import UUID

from src.domain.entities.refresh_token import RefreshToken


class RefreshTokenRepository(Protocol):
    async def add(self, token: RefreshToken) -> None: ...

    async def update(self, token: RefreshToken) -> None: ...

    async def get_by_hash(self, token_hash: bytes) -> RefreshToken | None: ...

    async def revoke_all_for_user(self, user_id: UUID, now: datetime) -> None: ...
