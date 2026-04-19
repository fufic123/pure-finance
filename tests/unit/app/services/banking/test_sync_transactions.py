from datetime import UTC, date, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.dtos.transaction_info import TransactionInfo
from src.app.services.banking.sync_transactions import SyncTransactions
from tests.fakes.clock import FixedClock
from tests.fakes.open_banking_provider import FakeOpenBankingProvider
from tests.fakes.repositories.fx_rate_repository import InMemoryFxRateRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.transaction_repository import InMemoryTransactionRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
_BOOKED = datetime(2026, 4, 18, 10, 0, 0, tzinfo=UTC)
_BOOKED_DATE = date(2026, 4, 18)


def _make_service(
    provider: FakeOpenBankingProvider | None = None,
    transactions: InMemoryTransactionRepository | None = None,
    fx_rates: InMemoryFxRateRepository | None = None,
) -> tuple[SyncTransactions, InMemoryTransactionRepository]:
    transactions = transactions or InMemoryTransactionRepository()
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        transactions=transactions,
        fx_rates=fx_rates or InMemoryFxRateRepository(),
    )
    service = SyncTransactions(
        uow_factory=lambda: uow,
        clock=FixedClock(_NOW),
        provider=provider or FakeOpenBankingProvider(),
    )
    return service, transactions


class TestSyncTransactions:
    @pytest.mark.asyncio
    async def test_adds_new_transactions(self) -> None:
        provider = FakeOpenBankingProvider(
            transactions=[
                TransactionInfo(
                    external_id="tx-1",
                    amount=Decimal("-12.50"),
                    currency="EUR",
                    description="Coffee",
                    booked_at=_BOOKED,
                ),
                TransactionInfo(
                    external_id="tx-2",
                    amount=Decimal("1000.00"),
                    currency="EUR",
                    description="Salary",
                    booked_at=_BOOKED,
                ),
            ]
        )
        service, repo = _make_service(provider=provider)
        account_id = uuid4()

        added = await service(account_id=account_id, account_external_id="acc-ext-1")

        assert added == 2
        stored = await repo.list_by_account(account_id)
        assert len(stored) == 2

    @pytest.mark.asyncio
    async def test_skips_already_synced_transactions(self) -> None:
        repo = InMemoryTransactionRepository()
        provider = FakeOpenBankingProvider(
            transactions=[
                TransactionInfo(
                    external_id="tx-1",
                    amount=Decimal("-5.00"),
                    currency="EUR",
                    description="Tea",
                    booked_at=_BOOKED,
                ),
            ]
        )
        service, _ = _make_service(provider=provider, transactions=repo)
        account_id = uuid4()

        await service(account_id=account_id, account_external_id="acc-ext-1")
        added = await service(account_id=account_id, account_external_id="acc-ext-1")

        assert added == 0
        stored = await repo.list_by_account(account_id)
        assert len(stored) == 1

    @pytest.mark.asyncio
    async def test_returns_zero_when_no_transactions(self) -> None:
        service, _ = _make_service()

        added = await service(account_id=uuid4(), account_external_id="acc-ext-1")

        assert added == 0

    @pytest.mark.asyncio
    async def test_eur_amount_set_when_currency_is_eur(self) -> None:
        provider = FakeOpenBankingProvider(
            transactions=[
                TransactionInfo(
                    external_id="tx-eur",
                    amount=Decimal("50.00"),
                    currency="EUR",
                    description="EUR payment",
                    booked_at=_BOOKED,
                )
            ]
        )
        service, repo = _make_service(provider=provider)

        await service(account_id=(aid := uuid4()), account_external_id="acc-1")

        stored = await repo.list_by_account(aid)
        assert stored[0].eur_amount == Decimal("50.00")

    @pytest.mark.asyncio
    async def test_eur_amount_converted_using_fx_rate(self) -> None:
        rates = InMemoryFxRateRepository(rates={("USD", _BOOKED_DATE): Decimal("1.10")})
        provider = FakeOpenBankingProvider(
            transactions=[
                TransactionInfo(
                    external_id="tx-usd",
                    amount=Decimal("110.00"),
                    currency="USD",
                    description="USD payment",
                    booked_at=_BOOKED,
                )
            ]
        )
        service, repo = _make_service(provider=provider, fx_rates=rates)

        await service(account_id=(aid := uuid4()), account_external_id="acc-1")

        stored = await repo.list_by_account(aid)
        assert stored[0].eur_amount == Decimal("100.0000")

    @pytest.mark.asyncio
    async def test_eur_amount_is_none_when_rate_missing(self) -> None:
        provider = FakeOpenBankingProvider(
            transactions=[
                TransactionInfo(
                    external_id="tx-gbp",
                    amount=Decimal("85.00"),
                    currency="GBP",
                    description="GBP payment",
                    booked_at=_BOOKED,
                )
            ]
        )
        service, repo = _make_service(provider=provider)

        await service(account_id=(aid := uuid4()), account_external_id="acc-1")

        stored = await repo.list_by_account(aid)
        assert stored[0].eur_amount is None
