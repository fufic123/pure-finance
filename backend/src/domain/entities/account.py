from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(slots=True)
class Account:
    id: UUID
    user_id: UUID
    connection_session_id: UUID
    institution_external_id: str
    external_id: str
    iban: str | None
    currency: str
    name: str
    created_at: datetime

    @classmethod
    def create(
        cls,
        user_id: UUID,
        connection_session_id: UUID,
        institution_external_id: str,
        external_id: str,
        iban: str | None,
        currency: str,
        name: str,
        now: datetime,
    ) -> "Account":
        return cls(
            id=uuid4(),
            user_id=user_id,
            connection_session_id=connection_session_id,
            institution_external_id=institution_external_id,
            external_id=external_id,
            iban=iban,
            currency=currency,
            name=name,
            created_at=now,
        )
