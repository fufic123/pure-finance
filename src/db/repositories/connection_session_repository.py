from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.connection_session import ConnectionSessionModel
from src.domain.entities.connection_session import ConnectionSession
from src.domain.enums.connection_status import ConnectionStatus


class PostgresConnectionSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, session: ConnectionSession) -> None:
        self._session.add(self._to_model(session))

    async def get_by_id(self, session_id: UUID) -> ConnectionSession | None:
        model = await self._session.get(ConnectionSessionModel, session_id)
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: ConnectionSessionModel) -> ConnectionSession:
        return ConnectionSession(
            id=model.id,
            user_id=model.user_id,
            institution_id=model.institution_id,
            requisition_id=model.requisition_id,
            link=model.link,
            redirect_uri=model.redirect_uri,
            status=ConnectionStatus(model.status),
            expires_at=model.expires_at,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: ConnectionSession) -> ConnectionSessionModel:
        return ConnectionSessionModel(
            id=entity.id,
            user_id=entity.user_id,
            institution_id=entity.institution_id,
            requisition_id=entity.requisition_id,
            link=entity.link,
            redirect_uri=entity.redirect_uri,
            status=entity.status.value,
            expires_at=entity.expires_at,
            created_at=entity.created_at,
        )
