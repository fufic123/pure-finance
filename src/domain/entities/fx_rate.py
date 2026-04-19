from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(slots=True)
class FxRate:
    id: UUID
    date: date
    currency: str  # quote currency; base is always EUR
    rate: Decimal  # units of currency per 1 EUR

    @classmethod
    def create(cls, date: date, currency: str, rate: Decimal) -> "FxRate":
        return cls(id=uuid4(), date=date, currency=currency, rate=rate)
