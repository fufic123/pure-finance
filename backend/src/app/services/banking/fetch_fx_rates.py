from typing import Callable

from src.app.ports.fx_rate_provider import FxRateProvider
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.fx_rate import FxRate


class FetchFxRates:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        provider: FxRateProvider,
    ) -> None:
        self._uow_factory = uow_factory
        self._provider = provider

    async def __call__(self) -> int:
        rate_date, rates_dict = await self._provider.get_rates()
        fx_rates = [
            FxRate.create(date=rate_date, currency=currency, rate=rate)
            for currency, rate in rates_dict.items()
        ]
        async with self._uow_factory() as uow:
            await uow.fx_rates.upsert_rates(fx_rates)
        return len(fx_rates)
