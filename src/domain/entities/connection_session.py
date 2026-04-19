from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from src.domain.enums.connection_status import ConnectionStatus


@dataclass(slots=True)
class ConnectionSession:
    id: UUID
    user_id: UUID
    institution_id: str
    requisition_id: str
    link: str
    redirect_uri: str
    status: ConnectionStatus
    expires_at: datetime
    created_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        institution_id: str,
        requisition_id: str,
        link: str,
        redirect_uri: str,
        now: datetime,
        lifetime_seconds: int,
    ) -> "ConnectionSession":
        return cls(
            id=uuid4(),
            user_id=user_id,
            institution_id=institution_id,
            requisition_id=requisition_id,
            link=link,
            redirect_uri=redirect_uri,
            status=ConnectionStatus.CREATED,
            expires_at=now + timedelta(seconds=lifetime_seconds),
            created_at=now,
        )

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    def mark_linked(self) -> None:
        self.status = ConnectionStatus.LINKED

    def mark_expired(self) -> None:
        self.status = ConnectionStatus.EXPIRED

    def mark_revoked(self) -> None:
        self.status = ConnectionStatus.REVOKED
