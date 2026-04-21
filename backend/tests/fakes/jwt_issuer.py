from datetime import datetime
from uuid import UUID

from src.app.exceptions.access_token_invalid import AccessTokenInvalid


class StubJwtIssuer:
    def __init__(self) -> None:
        self._by_token: dict[str, UUID] = {}
        self._counter = 0

    def issue(self, user_id: UUID, now: datetime) -> str:
        self._counter += 1
        token = f"access-{self._counter}"
        self._by_token[token] = user_id
        return token

    def verify(self, token: str, now: datetime) -> UUID:
        if token not in self._by_token:
            raise AccessTokenInvalid()
        return self._by_token[token]
