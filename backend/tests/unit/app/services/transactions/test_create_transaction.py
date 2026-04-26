from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.app.exceptions.account_not_found import AccountNotFound
from src.app.services.transactions.create_transaction import CreateTransaction
from src.db.models.account import Account
from src.db.models.categorization_rule import CategorizationRule
from tests.fakes.clock import FixedClock
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.categorization_rule_repository import InMemoryCategorizationRuleRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.transaction_repository import InMemoryTransactionRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


def _make_account(user_id) -> Account:
    return Account(
        id=uuid4(),
        user_id=user_id,
        iban=None,
        currency="EUR",
        name="Main",
        created_at=_NOW,
        balance=Decimal("0"),
    )


async def _make_uow(user_id, rules=None):
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=InMemoryAccountRepository(),
        transactions=InMemoryTransactionRepository(),
        categorization_rules=InMemoryCategorizationRuleRepository(rules),
    )
    account = _make_account(user_id)
    await uow.accounts.add(account)
    return uow, account


@pytest.mark.asyncio
async def test_creates_transaction() -> None:
    user_id = uuid4()
    uow, account = await _make_uow(user_id)
    service = CreateTransaction(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    tx = await service(
        user_id=user_id,
        account_id=account.id,
        amount=Decimal("-12.50"),
        currency="EUR",
        description="Coffee shop",
        booked_at=_NOW,
        category_id=None,
        note=None,
    )

    assert tx.account_id == account.id
    assert tx.amount == Decimal("-12.50")
    assert tx.description == "Coffee shop"
    assert tx.currency == "EUR"
    stored = await uow.transactions.get_by_id(tx.id)
    assert stored is not None


@pytest.mark.asyncio
async def test_auto_applies_first_matching_rule_case_insensitive() -> None:
    user_id = uuid4()
    cat_id_1 = uuid4()
    cat_id_2 = uuid4()
    rules = [
        CategorizationRule(
            id=uuid4(), user_id=user_id, category_id=cat_id_1,
            keyword="coffee", created_at=_NOW,
        ),
        CategorizationRule(
            id=uuid4(), user_id=user_id, category_id=cat_id_2,
            keyword="shop", created_at=_NOW,
        ),
    ]
    uow, account = await _make_uow(user_id, rules)
    service = CreateTransaction(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    tx = await service(
        user_id=user_id,
        account_id=account.id,
        amount=Decimal("-5"),
        currency="EUR",
        description="MORNING COFFEE AT THE SHOP",
        booked_at=_NOW,
        category_id=None,
        note=None,
    )

    assert tx.category_id == cat_id_1
    assert tx.manually_categorized is False


@pytest.mark.asyncio
async def test_no_rule_match_leaves_category_null() -> None:
    user_id = uuid4()
    rules = [
        CategorizationRule(
            id=uuid4(), user_id=user_id, category_id=uuid4(),
            keyword="netflix", created_at=_NOW,
        ),
    ]
    uow, account = await _make_uow(user_id, rules)
    service = CreateTransaction(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    tx = await service(
        user_id=user_id,
        account_id=account.id,
        amount=Decimal("-5"),
        currency="EUR",
        description="Coffee",
        booked_at=_NOW,
        category_id=None,
        note=None,
    )

    assert tx.category_id is None


@pytest.mark.asyncio
async def test_explicit_category_id_skips_rule_auto_apply() -> None:
    user_id = uuid4()
    rule_cat = uuid4()
    explicit = uuid4()
    rules = [
        CategorizationRule(
            id=uuid4(), user_id=user_id, category_id=rule_cat,
            keyword="coffee", created_at=_NOW,
        ),
    ]
    uow, account = await _make_uow(user_id, rules)
    service = CreateTransaction(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    tx = await service(
        user_id=user_id,
        account_id=account.id,
        amount=Decimal("-5"),
        currency="EUR",
        description="Coffee",
        booked_at=_NOW,
        category_id=explicit,
        note=None,
    )

    assert tx.category_id == explicit
    assert tx.manually_categorized is True


@pytest.mark.asyncio
async def test_raises_when_account_foreign() -> None:
    owner = uuid4()
    uow, account = await _make_uow(owner)
    service = CreateTransaction(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    with pytest.raises(AccountNotFound):
        await service(
            user_id=uuid4(),
            account_id=account.id,
            amount=Decimal("-1"),
            currency="EUR",
            description="x",
            booked_at=_NOW,
            category_id=None,
            note=None,
        )


@pytest.mark.asyncio
async def test_raises_when_account_missing() -> None:
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
    )
    service = CreateTransaction(uow_factory=lambda: uow, clock=FixedClock(_NOW))

    with pytest.raises(AccountNotFound):
        await service(
            user_id=uuid4(),
            account_id=uuid4(),
            amount=Decimal("-1"),
            currency="EUR",
            description="x",
            booked_at=_NOW,
            category_id=None,
            note=None,
        )
