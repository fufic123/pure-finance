from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.transaction import Transaction


class TransactionResponse(BaseModel):
    id: UUID
    amount: Decimal
    currency: str
    description: str
    booked_at: datetime

    @classmethod
    def from_transaction(cls, transaction: Transaction) -> "TransactionResponse":
        return cls(
            id=transaction.id,
            amount=transaction.amount,
            currency=transaction.currency,
            description=transaction.description,
            booked_at=transaction.booked_at,
        )
