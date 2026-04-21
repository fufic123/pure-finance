from datetime import UTC, datetime
from uuid import UUID, uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import get_current_user_service, get_rate_limiter
from src.api.main import create_app
from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.domain.entities.user import User
from tests.fakes.rate_limiter import AllowingRateLimiter


class StubGetCurrentUserService:
    def __init__(
        self,
        user: User | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._user = user
        self._raises = raises
        self.calls: list[str] = []

    async def __call__(self, access_token: str) -> User:
        self.calls.append(access_token)
        if self._raises is not None:
            raise self._raises
        assert self._user is not None
        return self._user


class TestGetUserRoute:
    def test_returns_user_on_valid_token(self) -> None:
        user = User(
            id=UUID("11111111-1111-1111-1111-111111111111"),
            google_id="g-1",
            email="m@example.com",
            created_at=datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC),
        )
        stub = StubGetCurrentUserService(user=user)
        client = _client_with(stub)

        response = client.get(
            "/api/user",
            headers={"Authorization": "Bearer valid-token"},
        )

        assert response.status_code == 200
        assert response.json() == {
            "id": "11111111-1111-1111-1111-111111111111",
            "email": "m@example.com",
            "created_at": "2026-04-19T12:00:00Z",
        }
        assert stub.calls == ["valid-token"]

    def test_returns_401_without_authorization_header(self) -> None:
        stub = StubGetCurrentUserService(user=_make_user())
        client = _client_with(stub)

        response = client.get("/api/user")

        assert response.status_code == 401

    def test_returns_401_for_wrong_scheme(self) -> None:
        stub = StubGetCurrentUserService(user=_make_user())
        client = _client_with(stub)

        response = client.get("/api/user", headers={"Authorization": "Basic abc"})

        assert response.status_code == 401

    def test_returns_401_when_service_rejects_token(self) -> None:
        stub = StubGetCurrentUserService(raises=AccessTokenInvalid())
        client = _client_with(stub)

        response = client.get(
            "/api/user",
            headers={"Authorization": "Bearer garbage"},
        )

        assert response.status_code == 401


def _client_with(stub: StubGetCurrentUserService) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_current_user_service] = lambda: stub
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    return TestClient(app)


def _make_user() -> User:
    return User(
        id=uuid4(),
        google_id="g-1",
        email="m@example.com",
        created_at=datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC),
    )
