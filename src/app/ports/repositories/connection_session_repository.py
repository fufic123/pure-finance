from typing import Protocol
from uuid import UUID

from src.domain.entities.connection_session import ConnectionSession


class ConnectionSessionRepository(Protocol):
    async def add(self, session: ConnectionSession) -> None: ...

    async def get_by_id(self, session_id: UUID) -> ConnectionSession | None: ...
