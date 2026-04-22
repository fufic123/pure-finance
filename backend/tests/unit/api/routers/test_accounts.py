from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_create_account,
    get_current_user,
    get_current_user_service,
    get_get_account_balance,
    get_rate_limiter,
    get_update_account,
)
from src.api.main import create_app
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.institution_not_found import InstitutionNotFound
from src.app.services.accounts.get_account_balance import AccountBalance
from src.domain.entities.account import Account
from src.domain.entities.user import User
from tests.fakes.rate_limiter import AllowingRateLimiter

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)
_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
_USER = User(id=_USER_ID, google_id="g-1", email="m@example.com", created_at=_NOW)


class _NoopGetCurrentUser:
    async def __call__(self, token: str) -> User:
        return _USER


class _StubCreateAccount:
    def __init__(
        self,
        account: Account | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._account = account
        self._raises = raises

    async def __call__(self, **kwargs) -> Account:
        if self._raises:
            raise self._raises
        return self._account or _make_account(user_id=kwargs["user_id"])


class _StubUpdateAccount:
    def __init__(
        self,
        account: Account | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._account = account
        self._raises = raises

    async def __call__(self, **kwargs) -> Account:
        if self._raises:
            raise self._raises
        return self._account or _make_account(user_id=kwargs["user_id"])


class _StubGetAccountBalance:
    def __init__(
        self,
        balance: AccountBalance | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._balance = balance
        self._raises = raises

    async def __call__(self, account_id, user_id) -> AccountBalance | None:
        if self._raises:
            raise self._raises
        return self._balance


def _make_account(user_id: UUID | None = None) -> Account:
    return Account(
        id=uuid4(),
        user_id=user_id or _USER_ID,
        iban=None,
        currency="EUR",
        name="Main",
        created_at=_NOW,
        institution_id=None,
        balance=Decimal("100.00"),
    )


def _base_overrides(app) -> None:
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    app.dependency_overrides[get_current_user_service] = lambda: _NoopGetCurrentUser()
    app.dependency_overrides[get_create_account] = lambda: _StubCreateAccount()
    app.dependency_overrides[get_update_account] = lambda: _StubUpdateAccount()
    app.dependency_overrides[get_get_account_balance] = lambda: _StubGetAccountBalance()


def _authed(**overrides) -> TestClient:
    app = create_app()
    _base_overrides(app)
    app.dependency_overrides[get_current_user] = lambda: _USER
    for dep, stub in overrides.items():
        app.dependency_overrides[dep] = lambda s=stub: s
    return TestClient(app)


class TestCreateAccountRoute:
    def test_returns_201_and_body(self) -> None:
        account = _make_account()
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_create_account] = lambda: _StubCreateAccount(account)
        client = TestClient(app)

        response = client.post(
            "/api/accounts",
            json={"name": "Main", "currency": "EUR", "balance": "100.00"},
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Main"
        assert Decimal(str(data["balance"])) == Decimal("100.00")

    def test_returns_404_when_institution_unknown(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_create_account] = lambda: _StubCreateAccount(raises=InstitutionNotFound())
        client = TestClient(app)

        response = client.post(
            "/api/accounts",
            json={
                "institution_id": str(uuid4()),
                "name": "Main",
                "currency": "EUR",
                "balance": "0",
            },
        )

        assert response.status_code == 404

    def test_rejects_non_eur_currency(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        client = TestClient(app)

        response = client.post(
            "/api/accounts",
            json={"name": "Main", "currency": "USD", "balance": "0"},
        )

        assert response.status_code == 422


class TestUpdateAccountRoute:
    def test_returns_200(self) -> None:
        account = _make_account()
        account.name = "Renamed"
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_update_account] = lambda: _StubUpdateAccount(account)
        client = TestClient(app)

        response = client.patch(f"/api/accounts/{account.id}", json={"name": "Renamed"})

        assert response.status_code == 200
        assert response.json()["name"] == "Renamed"

    def test_returns_404_when_account_not_owned(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_update_account] = lambda: _StubUpdateAccount(raises=AccountNotFound())
        client = TestClient(app)

        response = client.patch(f"/api/accounts/{uuid4()}", json={"name": "X"})

        assert response.status_code == 404


class TestGetAccountBalanceRoute:
    def test_returns_balance(self) -> None:
        balance = AccountBalance(
            amount=Decimal("500.00"),
            currency="EUR",
            updated_at=_NOW,
        )
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_get_account_balance] = lambda: _StubGetAccountBalance(balance=balance)
        client = TestClient(app)

        response = client.get(f"/api/accounts/{uuid4()}/balance")

        assert response.status_code == 200
        data = response.json()
        assert Decimal(str(data["amount"])) == Decimal("500.00")
        assert data["currency"] == "EUR"

    def test_returns_404_when_no_snapshot(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_get_account_balance] = lambda: _StubGetAccountBalance(balance=None)
        client = TestClient(app)

        response = client.get(f"/api/accounts/{uuid4()}/balance")

        assert response.status_code == 404

    def test_returns_404_when_not_owned(self) -> None:
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_get_account_balance] = lambda: _StubGetAccountBalance(raises=AccountNotFound())
        client = TestClient(app)

        response = client.get(f"/api/accounts/{uuid4()}/balance")

        assert response.status_code == 404
