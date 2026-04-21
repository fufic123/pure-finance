from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_analytics_by_category,
    get_analytics_summary,
    get_current_user,
    get_current_user_service,
    get_rate_limiter,
)
from src.api.main import create_app
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.services.analytics.get_by_category import CategoryTotal
from src.app.services.analytics.get_summary import AnalyticsSummary
from src.domain.entities.user import User
from tests.fakes.rate_limiter import AllowingRateLimiter

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
_USER = User(id=_USER_ID, google_id="g-1", email="m@example.com", created_at=_NOW)


class _NoopGetCurrentUser:
    async def __call__(self, token: str) -> User:
        return _USER


class _StubGetAnalyticsSummary:
    def __init__(
        self,
        result: AnalyticsSummary | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._result = result or AnalyticsSummary(
            income_eur=Decimal("0"),
            expenses_eur=Decimal("0"),
            net_eur=Decimal("0"),
            transaction_count=0,
            transactions_without_fx=0,
        )
        self._raises = raises

    async def __call__(self, user_id, **kwargs) -> AnalyticsSummary:
        if self._raises:
            raise self._raises
        return self._result


class _StubGetAnalyticsByCategory:
    def __init__(
        self,
        result: list[CategoryTotal] | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._result = result or []
        self._raises = raises

    async def __call__(self, user_id, **kwargs) -> list[CategoryTotal]:
        if self._raises:
            raise self._raises
        return self._result


def _base_overrides(app) -> None:
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    app.dependency_overrides[get_current_user_service] = lambda: _NoopGetCurrentUser()
    app.dependency_overrides[get_analytics_summary] = lambda: _StubGetAnalyticsSummary()
    app.dependency_overrides[get_analytics_by_category] = lambda: _StubGetAnalyticsByCategory()


def _authed_client(dep_overrides: dict | None = None) -> TestClient:
    app = create_app()
    _base_overrides(app)
    app.dependency_overrides[get_current_user] = lambda: _USER
    for dep, stub in (dep_overrides or {}).items():
        app.dependency_overrides[dep] = lambda s=stub: s
    return TestClient(app)


def _no_auth_client() -> TestClient:
    app = create_app()
    _base_overrides(app)
    return TestClient(app)


class TestGetSummaryRoute:
    def test_returns_summary(self) -> None:
        summary = AnalyticsSummary(
            income_eur=Decimal("500.00"),
            expenses_eur=Decimal("-300.00"),
            net_eur=Decimal("200.00"),
            transaction_count=10,
            transactions_without_fx=1,
        )
        client = _authed_client({get_analytics_summary: _StubGetAnalyticsSummary(result=summary)})

        response = client.get("/api/analytics/summary")

        assert response.status_code == 200
        data = response.json()
        assert Decimal(str(data["income_eur"])) == Decimal("500.00")
        assert Decimal(str(data["expenses_eur"])) == Decimal("-300.00")
        assert Decimal(str(data["net_eur"])) == Decimal("200.00")
        assert data["transaction_count"] == 10
        assert data["transactions_without_fx"] == 1

    def test_returns_404_when_account_not_owned(self) -> None:
        client = _authed_client(
            {get_analytics_summary: _StubGetAnalyticsSummary(raises=AccountNotFound())}
        )

        response = client.get(f"/api/analytics/summary?account_id={uuid4()}")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _no_auth_client().get("/api/analytics/summary")

        assert response.status_code == 401


class TestGetByCategoryRoute:
    def test_returns_category_totals(self) -> None:
        cat_id = uuid4()
        totals = [
            CategoryTotal(category_id=cat_id, total_eur=Decimal("-150.00"), count=5),
            CategoryTotal(category_id=None, total_eur=Decimal("-50.00"), count=2),
        ]
        client = _authed_client(
            {get_analytics_by_category: _StubGetAnalyticsByCategory(result=totals)}
        )

        response = client.get("/api/analytics/by-category")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert data[0]["category_id"] == str(cat_id)
        assert Decimal(str(data[0]["total_eur"])) == Decimal("-150.00")
        assert data[0]["count"] == 5
        assert data[1]["category_id"] is None

    def test_returns_404_when_account_not_owned(self) -> None:
        client = _authed_client(
            {get_analytics_by_category: _StubGetAnalyticsByCategory(raises=AccountNotFound())}
        )

        response = client.get(f"/api/analytics/by-category?account_id={uuid4()}")

        assert response.status_code == 404

    def test_returns_401_without_auth(self) -> None:
        response = _no_auth_client().get("/api/analytics/by-category")

        assert response.status_code == 401
