from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.connection_session import ConnectionSession


class ConnectionResponse(BaseModel):
    id: UUID
    institution_id: str
    status: str
    created_at: datetime

    @classmethod
    def from_session(cls, session: ConnectionSession) -> "ConnectionResponse":
        return cls(
            id=session.id,
            institution_id=session.institution_id,
            status=session.status,
            created_at=session.created_at,
        )
