from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_current_user,
    get_current_user_service,
    get_finalize_bank_connection,
    get_get_account,
    get_get_balance,
    get_list_accounts,
    get_list_connections,
    get_list_institutions,
    get_list_transactions,
    get_rate_limiter,
    get_revoke_connection,
    get_start_bank_connection,
    get_sync_account_balance,
    get_sync_transactions,
)
from src.api.main import create_app
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.connection_session_expired import ConnectionSessionExpired
from src.app.exceptions.connection_session_not_found import ConnectionSessionNotFound
from src.domain.entities.account import Account
from src.domain.entities.balance import Balance
from src.domain.entities.connection_session import ConnectionSession
from src.domain.entities.institution import Institution
from src.domain.entities.transaction import Transaction
from src.domain.entities.user import User
from src.domain.enums.connection_status import ConnectionStatus
from tests.fakes.rate_limiter import AllowingRateLimiter

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
_USER = User(id=_USER_ID, google_id="g-1", email="m@example.com", created_at=_NOW)


# --- stubs ---

class StubListInstitutions:
    def __init__(self, result: list[Institution] | None = None) -> None:
        self._result = result or []

    async def __call__(self, country: str) -> list[Institution]:
        return self._result


class StubStartBankConnection:
    def __init__(self, session: ConnectionSession | None = None) -> None:
        self._session = session or _make_session()

    async def __call__(self, user_id, institution_id, redirect_uri) -> ConnectionSession:
        return self._session


class StubFinalizeBankConnection:
    def __init__(
        self,
        accounts: list[Account] | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._accounts = accounts or []
        self._raises = raises

    async def __call__(self, session_id, user_id) -> list[Account]:
        if self._raises:
            raise self._raises
        return self._accounts


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

    async def __call__(self, account_id, user_id) -> list[Transaction]:
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


class StubSyncTransactions:
    def __init__(self, added: int = 0) -> None:
        self._added = added

    async def __call__(self, account_id, account_external_id, user_id) -> int:
        return self._added


class StubSyncAccountBalance:
    async def __call__(self, account_id, account_external_id) -> bool:
        return True


class StubGetBalance:
    def __init__(
        self,
        balance: Balance | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._balance = balance
        self._raises = raises

    async def __call__(self, account_id, user_id) -> Balance | None:
        if self._raises:
            raise self._raises
        return self._balance


class _StubListConnections:
    async def __call__(self, user_id) -> list:
        return []


class _StubRevokeConnection:
    async def __call__(self, session_id, user_id) -> None:
        pass


class _NoopGetCurrentUser:
    async def __call__(self, token: str) -> User:
        return _USER


# --- helpers ---

def _make_session() -> ConnectionSession:
    return ConnectionSession(
        id=uuid4(),
        user_id=_USER_ID,
        institution_id="REVOLUT_LT",
        requisition_id="req-1",
        link="https://ob.example.com/auth",
        redirect_uri="http://localhost/cb",
        status=ConnectionStatus.CREATED,
        expires_at=datetime(2026, 4, 19, 13, 0, 0, tzinfo=UTC),
        created_at=_NOW,
    )


def _make_account(user_id: UUID | None = None) -> Account:
    return Account(
        id=uuid4(),
        user_id=user_id or _USER_ID,
        connection_session_id=uuid4(),
        institution_external_id="REVOLUT_LT",
        external_id="acc-ext-1",
        iban="LT12 3456 7890 1234 5678",
        currency="EUR",
        name="Main",
        created_at=_NOW,
    )


def _base_overrides(app) -> None:
    """Override all container-sourced deps to avoid Settings validation in tests."""
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    app.dependency_overrides[get_current_user_service] = lambda: _NoopGetCurrentUser()
    app.dependency_overrides[get_list_institutions] = lambda: StubListInstitutions()
    app.dependency_overrides[get_start_bank_connection] = lambda: StubStartBankConnection()
    app.dependency_overrides[get_finalize_bank_connection] = lambda: StubFinalizeBankConnection()
    app.dependency_overrides[get_list_accounts] = lambda: StubListAccounts()
    app.dependency_overrides[get_list_transactions] = lambda: StubListTransactions()
    app.dependency_overrides[get_get_account] = lambda: StubGetAccount()
    app.dependency_overrides[get_sync_transactions] = lambda: StubSyncTransactions()
    app.dependency_overrides[get_sync_account_balance] = lambda: StubSyncAccountBalance()
    app.dependency_overrides[get_get_balance] = lambda: StubGetBalance()
    app.dependency_overrides[get_list_connections] = lambda: _StubListConnections()
    app.dependency_overrides[get_revoke_connection] = lambda: _StubRevokeConnection()


def _client_with(**service_overrides) -> TestClient:
    """Authenticated client with explicit service stubs."""
    _dep_map = {
        "institutions": get_list_institutions,
        "start": get_start_bank_connection,
        "finalize": get_finalize_bank_connection,
        "accounts": get_list_accounts,
        "transactions": get_list_transactions,
        "get_account": get_get_account,
        "sync": get_sync_transactions,
        "sync_balance": get_sync_account_balance,
        "balance": get_get_balance,
    }
    app = create_app()
    _base_overrides(app)
    app.dependency_overrides[get_current_user] = lambda: _USER
    for name, stub in service_overrides.items():
        app.dependency_overrides[_dep_map[name]] = lambda s=stub: s
    return TestClient(app)


def _client_no_auth() -> TestClient:
    """Client without get_current_user override — expects 401 responses."""
    app = create_app()
    _base_overrides(app)
    return TestClient(app)


# --- tests ---

class TestListInstitutionsRoute:
    def test_returns_institutions(self) -> None:
        inst = Institution.from_provider(
            external_id="REVOLUT_LT", name="Revolut", country="LT",
            logo_url="https://cdn.example.com/r.png",
        )
        client = _client_with(institutions=StubListInstitutions([inst]))

        response = client.get("/institutions?country=LT")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["id"] == "REVOLUT_LT"
        assert data[0]["name"] == "Revolut"

    def test_returns_empty_list(self) -> None:
        client = _client_with(institutions=StubListInstitutions([]))

        response = client.get("/institutions?country=XX")

        assert response.status_code == 200
        assert response.json() == []


class TestStartConnectionRoute:
    def test_returns_session_id_and_link(self) -> None:
        session = _make_session()
        client = _client_with(start=StubStartBankConnection(session))

        response = client.post(
            "/connections/start",
            json={"institution_id": "REVOLUT_LT", "redirect_uri": "http://localhost/cb"},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == str(session.id)
        assert data["link"] == "https://ob.example.com/auth"

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().post(
            "/connections/start",
            json={"institution_id": "REVOLUT_LT", "redirect_uri": "http://localhost/cb"},
        )

        assert response.status_code == 401


class TestFinalizeConnectionRoute:
    def test_returns_accounts_on_success(self) -> None:
        account = _make_account()
        client = _client_with(finalize=StubFinalizeBankConnection(accounts=[account]))

        response = client.post(f"/connections/{uuid4()}/finalize")

        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_returns_404_when_session_not_found(self) -> None:
        client = _client_with(
            finalize=StubFinalizeBankConnection(raises=ConnectionSessionNotFound())
        )

        response = client.post(f"/connections/{uuid4()}/finalize")

        assert response.status_code == 404

    def test_returns_410_when_session_expired(self) -> None:
        client = _client_with(
            finalize=StubFinalizeBankConnection(raises=ConnectionSessionExpired())
        )

        response = client.post(f"/connections/{uuid4()}/finalize")

        assert response.status_code == 410


class TestListAccountsRoute:
    def test_returns_accounts(self) -> None:
        account = _make_account()
        client = _client_with(accounts=StubListAccounts([account]))

        response = client.get("/accounts")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["currency"] == "EUR"

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().get("/accounts")

        assert response.status_code == 401


class TestListTransactionsRoute:
    def test_returns_transactions(self) -> None:
        account = _make_account()
        tx = Transaction(
            id=uuid4(),
            account_id=account.id,
            external_id="tx-1",
            amount=Decimal("-12.50"),
            currency="EUR",
            description="Coffee",
            booked_at=_NOW,
            created_at=_NOW,
        )
        client = _client_with(transactions=StubListTransactions(transactions=[tx]))

        response = client.get(f"/accounts/{account.id}/transactions")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert Decimal(str(data[0]["amount"])) == Decimal("-12.50")
        assert data[0]["currency"] == "EUR"

    def test_returns_404_when_account_not_found_or_not_owned(self) -> None:
        client = _client_with(
            transactions=StubListTransactions(raises=AccountNotFound())
        )

        response = client.get(f"/accounts/{uuid4()}/transactions")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().get(f"/accounts/{uuid4()}/transactions")

        assert response.status_code == 401


class TestGetAccountBalanceRoute:
    def test_returns_balance(self) -> None:
        account = _make_account()
        balance = Balance(
            account_id=account.id,
            amount=Decimal("1234.56"),
            currency="EUR",
            updated_at=_NOW,
        )
        client = _client_with(balance=StubGetBalance(balance=balance))

        response = client.get(f"/accounts/{account.id}/balance")

        assert response.status_code == 200
        data = response.json()
        assert Decimal(str(data["amount"])) == Decimal("1234.56")
        assert data["currency"] == "EUR"

    def test_returns_null_when_no_balance(self) -> None:
        client = _client_with(balance=StubGetBalance(balance=None))

        response = client.get(f"/accounts/{uuid4()}/balance")

        assert response.status_code == 200
        assert response.json() is None

    def test_returns_404_when_account_not_owned(self) -> None:
        client = _client_with(balance=StubGetBalance(raises=AccountNotFound()))

        response = client.get(f"/accounts/{uuid4()}/balance")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _client_no_auth().get(f"/accounts/{uuid4()}/balance")

        assert response.status_code == 401
