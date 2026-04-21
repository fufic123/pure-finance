from fastapi.testclient import TestClient

from src.api.dependencies import (
    AUTH_RATE_LIMIT,
    get_logout,
    get_rate_limiter,
)
from src.api.main import create_app
from tests.fakes.rate_limiter import InMemoryRateLimiter


class StubLogout:
    async def __call__(self, refresh_token: str) -> None:
        return None


class TestAuthRateLimiting:
    def test_allows_requests_up_to_limit(self) -> None:
        app, limiter = _app_with_limiter()
        client = TestClient(app)

        for _ in range(AUTH_RATE_LIMIT):
            response = client.post("/api/auth/logout", json={"refresh": "r"})
            assert response.status_code == 204

    def test_returns_429_after_limit(self) -> None:
        app, _ = _app_with_limiter()
        client = TestClient(app)

        for _ in range(AUTH_RATE_LIMIT):
            client.post("/api/auth/logout", json={"refresh": "r"})

        response = client.post("/api/auth/logout", json={"refresh": "r"})
        assert response.status_code == 429


def _app_with_limiter() -> tuple[object, InMemoryRateLimiter]:
    limiter = InMemoryRateLimiter()
    app = create_app()
    app.dependency_overrides[get_rate_limiter] = lambda: limiter
    app.dependency_overrides[get_logout] = lambda: StubLogout()
    return app, limiter
