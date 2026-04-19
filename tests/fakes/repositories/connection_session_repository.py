from uuid import UUID

from src.domain.entities.connection_session import ConnectionSession


class InMemoryConnectionSessionRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, ConnectionSession] = {}

    async def add(self, session: ConnectionSession) -> None:
        self._by_id[session.id] = session

    async def get_by_id(self, session_id: UUID) -> ConnectionSession | None:
        return self._by_id.get(session_id)
