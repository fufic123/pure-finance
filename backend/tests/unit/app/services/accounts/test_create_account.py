from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.services.accounts.create_account import CreateAccount
from tests.fakes.clock import FixedClock
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.balance_snapshot_repository import InMemoryBalanceSnapshotRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


def _make_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )


@pytest.mark.asyncio
async def test_creates_account_with_balance() -> None:
    uow = _make_uow()
    service = CreateAccount(uow_factory=lambda: uow, clock=FixedClock(_NOW))
    user_id = uuid4()

    account = await service(
        user_id=user_id,
        name="Main",
        currency="EUR",
        balance=Decimal("100.00"),
    )

    assert account.user_id == user_id
    assert account.name == "Main"
    assert account.currency == "EUR"
    assert account.balance == Decimal("100.00")

    snaps = await uow.balance_snapshots.list_by_account(account.id)
    assert snaps == []


@pytest.mark.asyncio
async def test_creates_account_with_zero_balance() -> None:
    uow = _make_uow()
    service = CreateAccount(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    account = await service(
        user_id=uuid4(),
        name="Savings",
        currency="EUR",
        balance=Decimal("0"),
    )

    assert account.balance == Decimal("0")
