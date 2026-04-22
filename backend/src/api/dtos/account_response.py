from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.account import Account


class AccountResponse(BaseModel):
    id: UUID
    institution_id: UUID | None
    iban: str | None
    currency: str
    name: str
    balance: Decimal
    created_at: datetime

    @classmethod
    def from_account(cls, account: Account) -> "AccountResponse":
        return cls(
            id=account.id,
            institution_id=account.institution_id,
            iban=account.iban,
            currency=account.currency,
            name=account.name,
            balance=account.balance,
            created_at=account.created_at,
        )
