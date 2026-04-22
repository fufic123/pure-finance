from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4


@dataclass(slots=True)
class Account:
    id: UUID
    user_id: UUID
    iban: str | None
    currency: str
    name: str
    created_at: datetime
    institution_id: UUID | None = field(default=None)
    balance: Decimal = field(default_factory=lambda: Decimal("0"))

    @classmethod
    def create(
        cls,
        user_id: UUID,
        iban: str | None,
        currency: str,
        name: str,
        now: datetime,
        institution_id: UUID | None = None,
        balance: Decimal = Decimal("0"),
    ) -> "Account":
        return cls(
            id=uuid4(),
            user_id=user_id,
            iban=iban,
            currency=currency,
            name=name,
            created_at=now,
            institution_id=institution_id,
            balance=balance,
        )

    def apply_snapshot(self, amount: Decimal) -> None:
        self.balance = amount

    def rename(self, name: str) -> None:
        self.name = name
