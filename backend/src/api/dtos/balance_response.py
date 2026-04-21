from decimal import Decimal

from pydantic import BaseModel

from src.domain.entities.balance import Balance


class BalanceResponse(BaseModel):
    amount: Decimal
    currency: str

    @classmethod
    def from_balance(cls, balance: Balance) -> "BalanceResponse":
        return cls(amount=balance.amount, currency=balance.currency)
