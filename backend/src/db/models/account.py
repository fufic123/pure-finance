from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class AccountModel(Base):
    __tablename__ = "accounts"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    institution_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("institutions.id"),
        nullable=True,
        index=True,
    )
    iban: Mapped[str | None] = mapped_column(String(34), nullable=True)
    currency: Mapped[str] = mapped_column(String(3))
    name: Mapped[str] = mapped_column(String(512))
    balance: Mapped[Decimal] = mapped_column(
        Numeric(precision=16, scale=2),
        default=Decimal("0"),
        server_default="0",
    )
    created_at: Mapped[datetime]
