from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(slots=True, frozen=True)
class TransactionInfo:
    external_id: str
    amount: Decimal
    currency: str
    description: str
    booked_at: datetime
