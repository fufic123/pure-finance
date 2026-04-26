from datetime import datetime
from decimal import Decimal
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    iban: Mapped[str | None] = mapped_column(String(34), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    name: Mapped[str] = mapped_column(String(512))
    balance: Mapped[Decimal] = mapped_column(Numeric(precision=16, scale=2), default=Decimal("0"), server_default="0")
    created_at: Mapped[datetime]

    @classmethod
    def create(
        cls,
        user_id: UUID,
        name: str,
        currency: str,
        now: datetime,
        iban: str | None = None,
        balance: Decimal = Decimal("0"),
    ) -> "Account":
        return cls(id=uuid7(), user_id=user_id, iban=iban, currency=currency, name=name, balance=balance, created_at=now)

    def update_balance(self, amount: Decimal) -> None:
        self.balance = amount

    def rename(self, name: str) -> None:
        self.name = name
