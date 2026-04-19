from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass(slots=True)
class Balance:
    account_id: UUID
    amount: Decimal
    currency: str
    updated_at: datetime
