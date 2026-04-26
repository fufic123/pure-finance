from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.services.accounts.take_daily_snapshots import TakeDailySnapshots
from src.db.models.account import Account
from tests.fakes.clock import FixedClock
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.balance_snapshot_repository import InMemoryBalanceSnapshotRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 21, 23, 59, 0, tzinfo=UTC)


def _make_uow() -> FakeUnitOfWork:
    return FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )


def _account(balance: Decimal = Decimal("100.00")) -> Account:
    return Account(
        id=uuid4(),
        user_id=uuid4(),
        iban=None,
        currency="EUR",
        name="Main",
        created_at=_NOW,
        balance=balance,
    )


@pytest.mark.asyncio
async def test_no_accounts_returns_zero() -> None:
    uow = _make_uow()
    service = TakeDailySnapshots(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    count = await service()

    assert count == 0
    assert uow.balance_snapshots._by_id == {}


@pytest.mark.asyncio
async def test_creates_one_snapshot_per_account() -> None:
    acc1 = _account(Decimal("500.00"))
    acc2 = _account(Decimal("1200.00"))
    uow = _make_uow()
    await uow.accounts.add(acc1)
    await uow.accounts.add(acc2)
    service = TakeDailySnapshots(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    count = await service()

    assert count == 2
    snaps1 = await uow.balance_snapshots.list_by_account(acc1.id)
    snaps2 = await uow.balance_snapshots.list_by_account(acc2.id)
    assert len(snaps1) == 1
    assert len(snaps2) == 1
    assert snaps1[0].amount == Decimal("500.00")
    assert snaps2[0].amount == Decimal("1200.00")


@pytest.mark.asyncio
async def test_snapshot_recorded_at_matches_clock() -> None:
    acc = _account()
    uow = _make_uow()
    await uow.accounts.add(acc)
    service = TakeDailySnapshots(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    await service()

    snap = await uow.balance_snapshots.latest(acc.id)
    assert snap is not None
    assert snap.recorded_at == _NOW


@pytest.mark.asyncio
async def test_uses_current_account_balance() -> None:
    acc = _account(Decimal("999.99"))
    uow = _make_uow()
    await uow.accounts.add(acc)
    service = TakeDailySnapshots(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    await service()

    snap = await uow.balance_snapshots.latest(acc.id)
    assert snap is not None
    assert snap.amount == Decimal("999.99")
