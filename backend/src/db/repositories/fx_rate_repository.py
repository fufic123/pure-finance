from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.fx_rate import FxRateModel
from src.domain.entities.fx_rate import FxRate


class PostgresFxRateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert_rates(self, rates: list[FxRate]) -> None:
        if not rates:
            return
        values = [
            {"id": r.id, "date": r.date, "currency": r.currency, "rate": r.rate}
            for r in rates
        ]
        stmt = (
            insert(FxRateModel)
            .values(values)
            .on_conflict_do_update(
                constraint="uq_fx_rates_date_currency",
                set_={"rate": insert(FxRateModel).excluded.rate},
            )
        )
        await self._session.execute(stmt)

    async def get_rate(self, currency: str, date: date) -> Decimal | None:
        stmt = select(FxRateModel.rate).where(
            FxRateModel.currency == currency,
            FxRateModel.date == date,
        )
        return (await self._session.execute(stmt)).scalar_one_or_none()
