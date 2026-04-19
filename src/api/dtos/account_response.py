from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.account import Account


class AccountResponse(BaseModel):
    id: UUID
    institution_external_id: str
    iban: str | None
    currency: str
    name: str
    created_at: datetime

    @classmethod
    def from_account(cls, account: Account) -> "AccountResponse":
        return cls(
            id=account.id,
            institution_external_id=account.institution_external_id,
            iban=account.iban,
            currency=account.currency,
            name=account.name,
            created_at=account.created_at,
        )
