from datetime import date
from decimal import Decimal

from src.domain.entities.fx_rate import FxRate


class InMemoryFxRateRepository:
    def __init__(self, rates: dict[tuple[str, date], Decimal] | None = None) -> None:
        self._rates: dict[tuple[str, date], Decimal] = rates or {}

    async def upsert_rates(self, rates: list[FxRate]) -> None:
        for r in rates:
            self._rates[(r.currency, r.date)] = r.rate

    async def get_rate(self, currency: str, date: date) -> Decimal | None:
        return self._rates.get((currency, date))
