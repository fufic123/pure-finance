from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import Date, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class FxRateModel(Base):
    __tablename__ = "fx_rates"
    __table_args__ = (UniqueConstraint("date", "currency", name="uq_fx_rates_date_currency"),)

    id: Mapped[UUID] = mapped_column(primary_key=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    currency: Mapped[str] = mapped_column(String(3))
    rate: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=6))
