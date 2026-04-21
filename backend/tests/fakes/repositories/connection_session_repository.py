from uuid import UUID

from src.domain.entities.connection_session import ConnectionSession


class InMemoryConnectionSessionRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, ConnectionSession] = {}

    async def add(self, session: ConnectionSession) -> None:
        self._by_id[session.id] = session

    async def get_by_id(self, session_id: UUID) -> ConnectionSession | None:
        return self._by_id.get(session_id)

    async def list_by_user(self, user_id: UUID) -> list[ConnectionSession]:
        from src.domain.enums.connection_status import ConnectionStatus
        return [s for s in self._by_id.values() if s.user_id == user_id and s.status == ConnectionStatus.LINKED]

    async def update_status(self, session: ConnectionSession) -> None:
        if session.id in self._by_id:
            self._by_id[session.id] = session
