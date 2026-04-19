from datetime import date
from decimal import Decimal
from typing import Protocol

from src.domain.entities.fx_rate import FxRate


class FxRateRepository(Protocol):
    async def upsert_rates(self, rates: list[FxRate]) -> None: ...

    async def get_rate(self, currency: str, date: date) -> Decimal | None:
        """Return units of `currency` per 1 EUR on `date`, or None if not found."""
        ...
