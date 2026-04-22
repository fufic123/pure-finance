from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.account import Account


class AccountResponse(BaseModel):
    id: UUID
    iban: str | None
    currency: str
    name: str
    created_at: datetime

    @classmethod
    def from_account(cls, account: Account) -> "AccountResponse":
        return cls(
            id=account.id,
            iban=account.iban,
            currency=account.currency,
            name=account.name,
            created_at=account.created_at,
        )
