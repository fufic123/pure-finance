from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.transaction import Transaction


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    amount: Decimal
    currency: str
    description: str
    booked_at: datetime
    category_id: UUID | None
    note: str | None
    manually_categorized: bool

    @classmethod
    def from_transaction(cls, transaction: Transaction) -> "TransactionResponse":
        return cls(
            id=transaction.id,
            account_id=transaction.account_id,
            amount=transaction.amount,
            currency=transaction.currency,
            description=transaction.description,
            booked_at=transaction.booked_at,
            category_id=transaction.category_id,
            note=transaction.note,
            manually_categorized=transaction.manually_categorized,
        )
