from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.connection_session import ConnectionSession


class StartConnectionResponse(BaseModel):
    session_id: UUID
    link: str

    @classmethod
    def from_session(cls, session: ConnectionSession) -> "StartConnectionResponse":
        return cls(session_id=session.id, link=session.link)
