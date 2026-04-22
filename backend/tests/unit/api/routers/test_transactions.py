from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_create_transaction,
    get_current_user,
    get_current_user_service,
    get_delete_transaction,
    get_list_transactions,
    get_rate_limiter,
    get_update_transaction,
)
from src.api.main import create_app
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.domain.entities.transaction import Transaction
from src.domain.entities.user import User
from tests.fakes.rate_limiter import AllowingRateLimiter

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)
_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
_USER = User(id=_USER_ID, google_id="g-1", email="m@example.com", created_at=_NOW)


class _NoopGetCurrentUser:
    async def __call__(self, token: str) -> User:
        return _USER


class _StubListTransactions:
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


class _StubCreateTransaction:
    def __init__(
        self,
        transaction: Transaction | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._transaction = transaction
        self._raises = raises

    async def __call__(self, **kwargs) -> Transaction:
        if self._raises:
            raise self._raises
        return self._transaction or _make_transaction()


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


class _StubDeleteTransaction:
    def __init__(self, raises: Exception | None = None) -> None:
        self._raises = raises

    async def __call__(self, transaction_id, user_id) -> None:
        if self._raises:
            raise self._raises


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


def _base_overrides(app) -> None:
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    app.dependency_overrides[get_current_user_service] = lambda: _NoopGetCurrentUser()
    app.dependency_overrides[get_list_transactions] = lambda: _StubListTransactions()
    app.dependency_overrides[get_create_transaction] = lambda: _StubCreateTransaction()
    app.dependency_overrides[get_update_transaction] = lambda: _StubUpdateTransaction()
    app.dependency_overrides[get_delete_transaction] = lambda: _StubDeleteTransaction()


def _authed():
    app = create_app()
    _base_overrides(app)
    app.dependency_overrides[get_current_user] = lambda: _USER
    return TestClient(app), app


def _no_auth_client() -> TestClient:
    app = create_app()
    _base_overrides(app)
    return TestClient(app)


class TestListTransactionsRoute:
    def test_returns_transactions(self) -> None:
        tx = _make_transaction()
        client, app = _authed()
        app.dependency_overrides[get_list_transactions] = lambda: _StubListTransactions([tx])

        response = client.get(f"/api/transactions?account_id={tx.account_id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert Decimal(str(data[0]["amount"])) == Decimal("-12.50")

    def test_returns_404_when_account_not_found_or_not_owned(self) -> None:
        client, app = _authed()
        app.dependency_overrides[get_list_transactions] = lambda: _StubListTransactions(
            raises=AccountNotFound()
        )

        response = client.get(f"/api/transactions?account_id={uuid4()}")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _no_auth_client().get(f"/api/transactions?account_id={uuid4()}")

        assert response.status_code == 401


class TestCreateTransactionRoute:
    def test_returns_201(self) -> None:
        tx = _make_transaction()
        client, app = _authed()
        app.dependency_overrides[get_create_transaction] = lambda: _StubCreateTransaction(tx)

        response = client.post(
            "/api/transactions",
            json={
                "account_id": str(tx.account_id),
                "amount": "-12.50",
                "currency": "EUR",
                "description": "Coffee",
                "booked_at": _NOW.isoformat(),
            },
        )

        assert response.status_code == 201
        assert Decimal(str(response.json()["amount"])) == Decimal("-12.50")

    def test_returns_404_when_account_foreign(self) -> None:
        client, app = _authed()
        app.dependency_overrides[get_create_transaction] = lambda: _StubCreateTransaction(
            raises=AccountNotFound()
        )

        response = client.post(
            "/api/transactions",
            json={
                "account_id": str(uuid4()),
                "amount": "-1",
                "currency": "EUR",
                "description": "X",
                "booked_at": _NOW.isoformat(),
            },
        )

        assert response.status_code == 404

    def test_rejects_non_eur(self) -> None:
        client, _ = _authed()

        response = client.post(
            "/api/transactions",
            json={
                "account_id": str(uuid4()),
                "amount": "-1",
                "currency": "USD",
                "description": "X",
                "booked_at": _NOW.isoformat(),
            },
        )

        assert response.status_code == 422


class TestUpdateTransactionRoute:
    def test_updates_note(self) -> None:
        tx = _make_transaction()
        tx.note = "groceries"
        client, app = _authed()
        app.dependency_overrides[get_update_transaction] = lambda: _StubUpdateTransaction(tx)

        response = client.patch(f"/api/transactions/{tx.id}", json={"note": "groceries"})

        assert response.status_code == 200
        assert response.json()["note"] == "groceries"

    def test_returns_404_when_not_found_or_not_owned(self) -> None:
        client, app = _authed()
        app.dependency_overrides[get_update_transaction] = lambda: _StubUpdateTransaction(
            raises=TransactionNotFound()
        )

        response = client.patch(f"/api/transactions/{uuid4()}", json={"note": "x"})

        assert response.status_code == 404


class TestDeleteTransactionRoute:
    def test_returns_204(self) -> None:
        client, _ = _authed()

        response = client.delete(f"/api/transactions/{uuid4()}")

        assert response.status_code == 204

    def test_returns_404_when_not_found(self) -> None:
        client, app = _authed()
        app.dependency_overrides[get_delete_transaction] = lambda: _StubDeleteTransaction(
            raises=TransactionNotFound()
        )

        response = client.delete(f"/api/transactions/{uuid4()}")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _no_auth_client().delete(f"/api/transactions/{uuid4()}")

        assert response.status_code == 401
