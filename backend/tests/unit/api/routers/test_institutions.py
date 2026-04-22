from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_current_user,
    get_current_user_service,
    get_list_institutions,
    get_rate_limiter,
)
from src.api.main import create_app
from src.domain.entities.institution import Institution
from src.domain.entities.user import User
from tests.fakes.rate_limiter import AllowingRateLimiter

_NOW = datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)
_USER_ID = UUID("11111111-1111-1111-1111-111111111111")
_USER = User(id=_USER_ID, google_id="g-1", email="m@example.com", created_at=_NOW)


class _StubListInstitutions:
    def __init__(self, items: list[Institution] | None = None) -> None:
        self._items = items or []

    async def __call__(self) -> list[Institution]:
        return self._items


class _NoopGetCurrentUser:
    async def __call__(self, token: str) -> User:
        return _USER


def _base_overrides(app) -> None:
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    app.dependency_overrides[get_current_user_service] = lambda: _NoopGetCurrentUser()
    app.dependency_overrides[get_list_institutions] = lambda: _StubListInstitutions()


class TestListInstitutionsRoute:
    def test_returns_list(self) -> None:
        items = [
            Institution(id=uuid4(), name="SEB", created_at=_NOW),
            Institution(id=uuid4(), name="Swedbank", created_at=_NOW),
        ]
        app = create_app()
        _base_overrides(app)
        app.dependency_overrides[get_current_user] = lambda: _USER
        app.dependency_overrides[get_list_institutions] = lambda: _StubListInstitutions(items)
        client = TestClient(app)

        response = client.get("/api/institutions")

        assert response.status_code == 200
        data = response.json()
        assert [i["name"] for i in data] == ["SEB", "Swedbank"]
        assert all("id" in i for i in data)

    def test_returns_401_without_auth(self) -> None:
        app = create_app()
        _base_overrides(app)
        client = TestClient(app)

        response = client.get("/api/institutions")

        assert response.status_code == 401
