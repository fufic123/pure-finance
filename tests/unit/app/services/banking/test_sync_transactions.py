from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.dtos.transaction_info import TransactionInfo
from src.app.services.banking.sync_transactions import SyncTransactions
from tests.fakes.clock import FixedClock
from tests.fakes.open_banking_provider import FakeOpenBankingProvider
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.transaction_repository import InMemoryTransactionRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
_BOOKED = datetime(2026, 4, 18, 10, 0, 0, tzinfo=UTC)


def _make_service(
    provider: FakeOpenBankingProvider | None = None,
    transactions: InMemoryTransactionRepository | None = None,
) -> tuple[SyncTransactions, InMemoryTransactionRepository]:
    transactions = transactions or InMemoryTransactionRepository()
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        transactions=transactions,
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
