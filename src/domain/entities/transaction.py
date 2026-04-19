from dataclasses import dataclass, field
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
    eur_amount: Decimal | None = field(default=None)
    category_id: UUID | None = field(default=None)
    note: str | None = field(default=None)
    manually_categorized: bool = field(default=False)

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

    def categorize(self, category_id: UUID, *, manually: bool) -> None:
        self.category_id = category_id
        self.manually_categorized = manually

    def set_note(self, note: str | None) -> None:
        self.note = note
