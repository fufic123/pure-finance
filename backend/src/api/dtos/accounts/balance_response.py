from decimal import Decimal

from pydantic import BaseModel


class BalanceResponse(BaseModel):
    amount: Decimal
    currency: str
