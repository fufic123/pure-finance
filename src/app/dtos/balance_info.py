from decimal import Decimal

from pydantic import BaseModel


class BalanceInfo(BaseModel, frozen=True):
    amount: Decimal
    currency: str
