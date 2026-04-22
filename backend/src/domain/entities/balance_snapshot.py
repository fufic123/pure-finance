from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from src.app.ports.clock import Clock


@dataclass(slots=True)
class BalanceSnapshot:
    id: UUID
    account_id: UUID
    amount: Decimal
    recorded_at: datetime
    created_at: datetime

    @classmethod
    def create(
        cls,
        account_id: UUID,
        amount: Decimal,
        recorded_at: datetime,
        clock: Clock,
    ) -> "BalanceSnapshot":
        if recorded_at.tzinfo is None:
            raise ValueError("recorded_at must be timezone-aware")
        return cls(
            id=uuid4(),
            account_id=account_id,
            amount=amount,
            recorded_at=recorded_at,
            created_at=clock.now(),
        )
