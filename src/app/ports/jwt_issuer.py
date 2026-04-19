from datetime import datetime
from typing import Protocol
from uuid import UUID


class JwtIssuer(Protocol):
    def issue(self, user_id: UUID, now: datetime) -> str: ...

    def verify(self, token: str, now: datetime) -> UUID: ...
