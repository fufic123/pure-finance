from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class CreateAccountRequest(BaseModel):
    institution_id: UUID | None = None
    name: str = Field(min_length=1, max_length=60)
    currency: str = "EUR"
    balance: Decimal

    @field_validator("currency")
    @classmethod
    def _currency_must_be_eur(cls, value: str) -> str:
        if value != "EUR":
            raise ValueError("currency must be EUR")
        return value
