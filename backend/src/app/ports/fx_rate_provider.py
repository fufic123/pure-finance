from datetime import date
from decimal import Decimal
from typing import Protocol


class FxRateProvider(Protocol):
    async def get_rates(self) -> tuple[date, dict[str, Decimal]]:
        """Return (date, {currency_code: units_per_eur}) for the latest available day."""
        ...
