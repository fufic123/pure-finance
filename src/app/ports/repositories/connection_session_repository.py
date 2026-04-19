from typing import Protocol
from uuid import UUID

from src.domain.entities.connection_session import ConnectionSession


class ConnectionSessionRepository(Protocol):
    async def add(self, session: ConnectionSession) -> None: ...

    async def get_by_id(self, session_id: UUID) -> ConnectionSession | None: ...

    async def list_by_user(self, user_id: UUID) -> list[ConnectionSession]: ...

    async def update_status(self, session: ConnectionSession) -> None: ...
