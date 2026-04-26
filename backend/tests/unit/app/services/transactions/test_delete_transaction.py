from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.app.services.transactions.delete_transaction import DeleteTransaction
from src.db.models.account import Account
from src.db.models.transaction import Transaction
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.transaction_repository import InMemoryTransactionRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


async def _setup(user_id, tx_user_id=None):
    tx_user_id = tx_user_id or user_id
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        transactions=InMemoryTransactionRepository(),
    )
    account = Account(
        id=uuid4(),
        user_id=tx_user_id,
        iban=None,
        currency="EUR",
        name="Main",
        created_at=_NOW,
        balance=Decimal("0"),
    )
    await uow.accounts.add(account)
    tx = Transaction(
        id=uuid4(),
        account_id=account.id,
        amount=Decimal("-5"),
        currency="EUR",
        description="x",
        booked_at=_NOW,
        created_at=_NOW,
    )
    await uow.transactions.add(tx)
    return uow, tx


@pytest.mark.asyncio
async def test_deletes_owned_transaction() -> None:
    user_id = uuid4()
    uow, tx = await _setup(user_id)
    service = DeleteTransaction(uow_factory=lambda: uow)

    await service(transaction_id=tx.id, user_id=user_id)

    assert await uow.transactions.get_by_id(tx.id) is None


@pytest.mark.asyncio
async def test_raises_when_transaction_missing() -> None:
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
    )
    service = DeleteTransaction(uow_factory=lambda: uow)

    with pytest.raises(TransactionNotFound):
        await service(transaction_id=uuid4(), user_id=uuid4())


@pytest.mark.asyncio
async def test_raises_when_transaction_on_foreign_account() -> None:
    owner = uuid4()
    other = uuid4()
    uow, tx = await _setup(owner, tx_user_id=owner)
    service = DeleteTransaction(uow_factory=lambda: uow)

    with pytest.raises(TransactionNotFound):
        await service(transaction_id=tx.id, user_id=other)
