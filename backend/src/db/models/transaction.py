from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class TransactionModel(Base):
    __tablename__ = "transactions"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
        index=True,
    )
    external_id: Mapped[str | None] = mapped_column(String(256), nullable=True, index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=4))
    currency: Mapped[str] = mapped_column(String(3))
    description: Mapped[str] = mapped_column(String(1024))
    booked_at: Mapped[datetime]
    created_at: Mapped[datetime]
    category_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    note: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    manually_categorized: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
