from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.services.accounts.update_account import UpdateAccount
from src.domain.entities.account import Account
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.balance_snapshot_repository import InMemoryBalanceSnapshotRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


def _make_uow(account: Account) -> FakeUnitOfWork:
    accounts = InMemoryAccountRepository()
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=accounts,
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )
    import asyncio
    asyncio.get_event_loop().run_until_complete(accounts.add(account)) if False else None
    return uow


def _account(user_id, balance=Decimal("100.00"), name="Main") -> Account:
    return Account(
        id=uuid4(),
        user_id=user_id,
        iban=None,
        currency="EUR",
        name=name,
        created_at=_NOW,
        institution_id=None,
        balance=balance,
    )


@pytest.mark.asyncio
async def test_updates_name_only() -> None:
    user_id = uuid4()
    account = _account(user_id)
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )
    await uow.accounts.add(account)

    service = UpdateAccount(uow_factory=lambda: uow)
    updated = await service(
        account_id=account.id,
        user_id=user_id,
        name="Renamed",
        balance=None,
        name_provided=True,
        balance_provided=False,
    )

    assert updated.name == "Renamed"
    assert updated.balance == Decimal("100.00")


@pytest.mark.asyncio
async def test_updates_balance() -> None:
    user_id = uuid4()
    account = _account(user_id)
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )
    await uow.accounts.add(account)

    service = UpdateAccount(uow_factory=lambda: uow)
    updated = await service(
        account_id=account.id,
        user_id=user_id,
        name=None,
        balance=Decimal("250.00"),
        name_provided=False,
        balance_provided=True,
    )

    assert updated.name == "Main"
    assert updated.balance == Decimal("250.00")
    snaps = await uow.balance_snapshots.list_by_account(account.id)
    assert snaps == []


@pytest.mark.asyncio
async def test_updates_name_and_balance() -> None:
    user_id = uuid4()
    account = _account(user_id)
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )
    await uow.accounts.add(account)

    service = UpdateAccount(uow_factory=lambda: uow)
    updated = await service(
        account_id=account.id,
        user_id=user_id,
        name="Newname",
        balance=Decimal("500.00"),
        name_provided=True,
        balance_provided=True,
    )

    assert updated.name == "Newname"
    assert updated.balance == Decimal("500.00")


@pytest.mark.asyncio
async def test_raises_when_account_foreign() -> None:
    account = _account(uuid4())
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )
    await uow.accounts.add(account)

    service = UpdateAccount(uow_factory=lambda: uow)
    with pytest.raises(AccountNotFound):
        await service(
            account_id=account.id,
            user_id=uuid4(),
            name="X",
            balance=None,
            name_provided=True,
            balance_provided=False,
        )


@pytest.mark.asyncio
async def test_raises_when_account_missing() -> None:
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
    )

    service = UpdateAccount(uow_factory=lambda: uow)
    with pytest.raises(AccountNotFound):
        await service(
            account_id=uuid4(),
            user_id=uuid4(),
            name="X",
            balance=None,
            name_provided=True,
            balance_provided=False,
        )
