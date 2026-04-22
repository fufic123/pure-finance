from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateTransactionRequest(BaseModel):
    account_id: UUID
    amount: Decimal
    currency: str = "EUR"
    description: str = Field(min_length=1, max_length=200)
    booked_at: datetime
    category_id: UUID | None = None
    note: str | None = Field(default=None, max_length=500)

    @field_validator("currency")
    @classmethod
    def _currency_must_be_eur(cls, value: str) -> str:
        if value != "EUR":
            raise ValueError("currency must be EUR")
        return value
