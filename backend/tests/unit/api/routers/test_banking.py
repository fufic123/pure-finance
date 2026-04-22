from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_create_account,
    get_current_user,
    get_current_user_service,
    get_delete_account,
    get_get_account,
    get_get_account_balance,
    get_list_accounts,
    get_list_transactions,
    get_rate_limiter,
    get_update_account,
    get_update_transaction,
)
from src.api.main import create_app
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.domain.entities.account import Account
from src.domain.entities.transaction import Transaction
from src.domain.entities.user import User
from tests.fakes.rate_limiter import AllowingRateLimiter

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
_USER = User(id=_USER_ID, google_id="g-1", email="m@example.com", created_at=_NOW)


# --- stubs ---


class StubListAccounts:
    def __init__(self, accounts: list[Account] | None = None) -> None:
        self._accounts = accounts or []

    async def __call__(self, user_id) -> list[Account]:
        return self._accounts


class StubListTransactions:
    def __init__(
        self,
        transactions: list[Transaction] | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._transactions = transactions or []
        self._raises = raises

    async def __call__(self, account_id, user_id, **kwargs) -> list[Transaction]:
        if self._raises:
            raise self._raises
        return self._transactions


class StubGetAccount:
    def __init__(self, account: Account | None = None, raises: Exception | None = None) -> None:
        self._account = account
        self._raises = raises

    async def __call__(self, account_id, user_id) -> Account:
        if self._raises:
            raise self._raises
        return self._account or _make_account(user_id=user_id)


class _StubDeleteAccount:
    def __init__(self, raises: Exception | None = None) -> None:
        self._raises = raises

    async def __call__(self, account_id, user_id) -> None:
        if self._raises:
            raise self._raises


class _StubUpdateTransaction:
    def __init__(
        self,
        transaction: Transaction | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._transaction = transaction
        self._raises = raises

    async def __call__(self, transaction_id, user_id, **kwargs) -> Transaction:
        if self._raises:
            raise self._raises
        return self._transaction or _make_transaction()


class _NoopGetCurrentUser:
    async def __call__(self, token: str) -> User:
        return _USER


# --- helpers ---


def _make_transaction(account_id: UUID | None = None) -> Transaction:
    return Transaction(
        id=uuid4(),
        account_id=account_id or uuid4(),
        amount=Decimal("-12.50"),
        currency="EUR",
        description="Coffee",
        booked_at=_NOW,
        created_at=_NOW,
    )


def _make_account(user_id: UUID | None = None) -> Account:
    return Account(
        id=uuid4(),
        user_id=user_id or _USER_ID,
        iban="LT12 3456 7890 1234 5678",
        currency="EUR",
        name="Main",
        created_at=_NOW,
    )


def _base_overrides(app) -> None:
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    app.dependency_overrides[get_current_user_service] = lambda: _NoopGetCurrentUser()
    app.dependency_overrides[get_list_accounts] = lambda: StubListAccounts()
    app.dependency_overrides[get_list_transactions] = lambda: StubListTransactions()
    app.dependency_overrides[get_get_account] = lambda: StubGetAccount()
    app.dependency_overrides[get_delete_account] = lambda: _StubDeleteAccount()
    app.dependency_overrides[get_update_transaction] = lambda: _StubUpdateTransaction()

    class _NoopCreate:
        async def __call__(self, **kwargs):
            raise AssertionError("should not be called")

    class _NoopUpdate:
        async def __call__(self, **kwargs):
            raise AssertionError("should not be called")

    class _NoopBalance:
        async def __call__(self, account_id, user_id):
            raise AssertionError("should not be called")

    app.dependency_overrides[get_create_account] = lambda: _NoopCreate()
    app.dependency_overrides[get_update_account] = lambda: _NoopUpdate()
    app.dependency_overrides[get_get_account_balance] = lambda: _NoopBalance()


def _client_with(**service_overrides) -> TestClient:
    _dep_map = {
        "accounts": get_list_accounts,
        "transactions": get_list_transactions,
        "get_account": get_get_account,
    }
    app = create_app()
    _base_overrides(app)
    app.dependency_overrides[get_current_user] = lambda: _USER
    for name, stub in service_overrides.items():
        app.dependency_overrides[_dep_map[name]] = lambda s=stub: s
    return TestClient(app)


def _client_no_auth() -> TestClient:
    app = create_app()
    _base_overrides(app)
    return TestClient(app)


# --- tests ---


class TestListAccountsRoute:
    def test_returns_accounts(self) -> None:
        account = _make_account()
        client = _client_with(accounts=StubListAccounts([account]))

        response = client.get("/api/accounts")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["currency"] == "EUR"

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().get("/api/accounts")

        assert response.status_code == 401


class TestListTransactionsRoute:
    def test_returns_transactions(self) -> None:
        account = _make_account()
        tx = Transaction(
            id=uuid4(),
            account_id=account.id,
            amount=Decimal("-12.50"),
            currency="EUR",
            description="Coffee",
            booked_at=_NOW,
            created_at=_NOW,
        )
        client = _client_with(transactions=StubListTransactions(transactions=[tx]))

        response = client.get(f"/api/transactions?account_id={account.id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert Decimal(str(data[0]["amount"])) == Decimal("-12.50")
        assert data[0]["currency"] == "EUR"

    def test_returns_404_when_account_not_found_or_not_owned(self) -> None:
        client = _client_with(
            transactions=StubListTransactions(raises=AccountNotFound())
        )

        response = client.get(f"/api/transactions?account_id={uuid4()}")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().get(f"/api/transactions?account_id={uuid4()}")

        assert response.status_code == 401


class TestDeleteAccountRoute:
    def test_deletes_account(self) -> None:
        account_id = uuid4()
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        client = TestClient(app)

        response = client.delete(f"/api/accounts/{account_id}")

        assert response.status_code == 204

    def test_returns_404_when_account_not_owned(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_delete_account] = lambda: _StubDeleteAccount(raises=AccountNotFound())
        client = TestClient(app)

        response = client.delete(f"/api/accounts/{uuid4()}")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().delete(f"/api/accounts/{uuid4()}")

        assert response.status_code == 401


class TestUpdateTransactionRoute:
    def test_updates_note(self) -> None:
        tx = _make_transaction()
        tx.note = "groceries"
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_update_transaction] = lambda: _StubUpdateTransaction(transaction=tx)
        client = TestClient(app)

        response = client.patch(f"/api/transactions/{tx.id}", json={"note": "groceries"})

        assert response.status_code == 200
        assert response.json()["note"] == "groceries"

    def test_returns_404_when_not_found_or_not_owned(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_update_transaction] = lambda: _StubUpdateTransaction(raises=TransactionNotFound())
        client = TestClient(app)

        response = client.patch(f"/api/transactions/{uuid4()}", json={"note": "x"})

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().patch(f"/api/transactions/{uuid4()}", json={"note": "x"})

        assert response.status_code == 401
