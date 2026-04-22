from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.exceptions.institution_not_found import InstitutionNotFound
from src.app.services.accounts.create_account import CreateAccount
from src.domain.entities.institution import Institution
from tests.fakes.clock import FixedClock
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.balance_snapshot_repository import InMemoryBalanceSnapshotRepository
from tests.fakes.repositories.institution_repository import InMemoryInstitutionRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


def _make_uow(institutions: list[Institution] | None = None) -> FakeUnitOfWork:
    return FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        balance_snapshots=InMemoryBalanceSnapshotRepository(),
        institutions=InMemoryInstitutionRepository(institutions),
    )


@pytest.mark.asyncio
async def test_creates_account_and_first_snapshot() -> None:
    uow = _make_uow()
    service = CreateAccount(uow_factory=lambda: uow, clock=FixedClock(_NOW))
    user_id = uuid4()

    account = await service(
        user_id=user_id,
        institution_id=None,
        name="Main",
        currency="EUR",
        balance=Decimal("100.00"),
    )

    assert account.user_id == user_id
    assert account.name == "Main"
    assert account.currency == "EUR"
    assert account.balance == Decimal("100.00")
    assert account.institution_id is None

    snaps = await uow.balance_snapshots.list_by_account(account.id)
    assert len(snaps) == 1
    assert snaps[0].amount == Decimal("100.00")


@pytest.mark.asyncio
async def test_assigns_institution_when_provided() -> None:
    inst = Institution(id=uuid4(), name="SEB", created_at=_NOW)
    uow = _make_uow([inst])
    service = CreateAccount(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    account = await service(
        user_id=uuid4(),
        institution_id=inst.id,
        name="Main",
        currency="EUR",
        balance=Decimal("0"),
    )

    assert account.institution_id == inst.id


@pytest.mark.asyncio
async def test_raises_when_institution_unknown() -> None:
    uow = _make_uow()
    service = CreateAccount(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    with pytest.raises(InstitutionNotFound):
        await service(
            user_id=uuid4(),
            institution_id=uuid4(),
            name="Main",
            currency="EUR",
            balance=Decimal("0"),
        )


@pytest.mark.asyncio
async def test_snapshot_uses_initial_balance_even_when_zero() -> None:
    uow = _make_uow()
    service = CreateAccount(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    account = await service(
        user_id=uuid4(),
        institution_id=None,
        name="Zero",
        currency="EUR",
        balance=Decimal("0"),
    )

    snaps = await uow.balance_snapshots.list_by_account(account.id)
    assert len(snaps) == 1
    assert snaps[0].amount == Decimal("0")
