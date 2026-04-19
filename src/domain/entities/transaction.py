from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(slots=True)
class Transaction:
    id: UUID
    account_id: UUID
    external_id: str
    amount: Decimal
    currency: str
    description: str
    booked_at: datetime
    created_at: datetime

    @classmethod
    def create(
        cls,
        account_id: UUID,
        external_id: str,
        amount: Decimal,
        currency: str,
        description: str,
        booked_at: datetime,
        now: datetime,
    ) -> "Transaction":
        return cls(
            id=uuid4(),
            account_id=account_id,
            external_id=external_id,
            amount=amount,
            currency=currency,
            description=description,
            booked_at=booked_at,
            created_at=now,
        )
