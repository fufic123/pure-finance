from decimal import Decimal

from pydantic import BaseModel, Field


class UpdateAccountRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=60)
    balance: Decimal | None = None
