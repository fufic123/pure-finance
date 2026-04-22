from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Index, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class BalanceSnapshotModel(Base):
    __tablename__ = "balance_snapshots"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    account_id: Mapped[UUID] = mapped_column(
        ForeignKey("accounts.id", ondelete="CASCADE"),
    )
    amount: Mapped[Decimal] = mapped_column(Numeric(precision=16, scale=2))
    recorded_at: Mapped[datetime]
    created_at: Mapped[datetime]

    __table_args__ = (
        Index(
            "ix_balance_snapshots_account_recorded_desc",
            "account_id",
            "recorded_at",
        ),
    )
