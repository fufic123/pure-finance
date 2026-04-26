from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    account_id: Mapped[UUID] = mapped_column(ForeignKey("accounts.id", ondelete="CASCADE"), index=True)
    external_id: Mapped[str | None] = mapped_column(String(256), nullable=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=4))
    currency: Mapped[str] = mapped_column(String(3))
    description: Mapped[str] = mapped_column(String(1024))
    booked_at: Mapped[datetime]
    created_at: Mapped[datetime]
    category_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    note: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    manually_categorized: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    @classmethod
    def create(
        cls,
        account_id: UUID,
        amount: Decimal,
        currency: str,
        description: str,
        booked_at: datetime,
        now: datetime,
        external_id: str | None = None,
    ) -> "Transaction":
        return cls(
            id=uuid4(),
            account_id=account_id,
            amount=amount,
            currency=currency,
            description=description,
            booked_at=booked_at,
            created_at=now,
            external_id=external_id,
            manually_categorized=False,
        )

    def categorize(self, category_id: UUID | None, *, manually: bool) -> None:
        self.category_id = category_id
        self.manually_categorized = manually

    def set_note(self, note: str | None) -> None:
        self.note = note
