from uuid import uuid4

from fastapi.testclient import TestClient

from src.api.dependencies import (
    get_google_callback,
    get_logout,
    get_rate_limiter,
    get_refresh_tokens,
    get_start_google_auth,
)
from src.api.main import create_app
from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid
from src.app.services.auth.token_pair import TokenPair
from src.app.exceptions.refresh_token_revoked import RefreshTokenRevoked
from tests.fakes.rate_limiter import AllowingRateLimiter


class StubStartGoogleAuth:
    def __init__(self, url: str) -> None:
        self._url = url
        self.calls: list[str] = []

    async def __call__(self, redirect_uri: str) -> str:
        self.calls.append(redirect_uri)
        return self._url


class StubGoogleCallback:
    def __init__(
        self,
        pair: TokenPair | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._pair = pair
        self._raises = raises
        self.calls: list[tuple[str, str, str]] = []

    async def __call__(self, code: str, redirect_uri: str, state: str) -> TokenPair:
        self.calls.append((code, redirect_uri, state))
        if self._raises is not None:
            raise self._raises
        assert self._pair is not None
        return self._pair


class StubRefreshTokens:
    def __init__(
        self,
        pair: TokenPair | None = None,
        raises: Exception | None = None,
    ) -> None:
        self._pair = pair
        self._raises = raises
        self.calls: list[str] = []

    async def __call__(self, refresh_token: str) -> TokenPair:
        self.calls.append(refresh_token)
        if self._raises is not None:
            raise self._raises
        assert self._pair is not None
        return self._pair


class StubLogout:
    def __init__(self) -> None:
        self.calls: list[str] = []

    async def __call__(self, refresh_token: str) -> None:
        self.calls.append(refresh_token)


class TestStartGoogleAuthRoute:
    def test_returns_authorization_url(self) -> None:
        stub = StubStartGoogleAuth("https://accounts.google.com/o/oauth2/v2/auth?x=y")
        client = _client_with(get_start_google_auth, stub)

        response = client.post(
            "/api/auth/google",
            json={"redirect_uri": "http://localhost/cb"},
        )

        assert response.status_code == 200
        assert response.json() == {
            "authorization_url": "https://accounts.google.com/o/oauth2/v2/auth?x=y"
        }
        assert stub.calls == ["http://localhost/cb"]


class TestGoogleCallbackRoute:
    def test_returns_token_pair_on_success(self) -> None:
        stub = StubGoogleCallback(TokenPair(access="a", refresh="r"))
        client = _client_with(get_google_callback, stub)

        response = client.post(
            "/api/auth/google/callback",
            json={
                "code": "abc",
                "redirect_uri": "http://localhost/cb",
                "state": "valid-state",
            },
        )

        assert response.status_code == 200
        assert response.json() == {"access": "a", "refresh": "r"}
        assert stub.calls == [("abc", "http://localhost/cb", "valid-state")]

    def test_returns_422_on_missing_code(self) -> None:
        stub = StubGoogleCallback(TokenPair(access="a", refresh="r"))
        client = _client_with(get_google_callback, stub)

        response = client.post(
            "/api/auth/google/callback",
            json={"redirect_uri": "http://localhost/cb", "state": "s"},
        )

        assert response.status_code == 422

    def test_returns_400_on_invalid_state(self) -> None:
        stub = StubGoogleCallback(raises=OAuthStateInvalid())
        client = _client_with(get_google_callback, stub)

        response = client.post(
            "/api/auth/google/callback",
            json={
                "code": "abc",
                "redirect_uri": "http://localhost/cb",
                "state": "tampered",
            },
        )

        assert response.status_code == 400


class TestRefreshRoute:
    def test_returns_new_token_pair(self) -> None:
        stub = StubRefreshTokens(pair=TokenPair(access="new-a", refresh="new-r"))
        client = _client_with(get_refresh_tokens, stub)

        response = client.post("/api/auth/refresh", json={"refresh": "old-r"})

        assert response.status_code == 200
        assert response.json() == {"access": "new-a", "refresh": "new-r"}
        assert stub.calls == ["old-r"]

    def test_returns_401_on_revoked_token(self) -> None:
        stub = StubRefreshTokens(raises=RefreshTokenRevoked(uuid4()))
        client = _client_with(get_refresh_tokens, stub)

        response = client.post("/api/auth/refresh", json={"refresh": "stolen"})

        assert response.status_code == 401


class TestLogoutRoute:
    def test_returns_204_on_success(self) -> None:
        stub = StubLogout()
        client = _client_with(get_logout, stub)

        response = client.post("/api/auth/logout", json={"refresh": "r"})

        assert response.status_code == 204
        assert stub.calls == ["r"]


def _client_with(dependency, stub) -> TestClient:
    app = create_app()
    app.dependency_overrides[dependency] = lambda: stub
    app.dependency_overrides[get_rate_limiter] = lambda: AllowingRateLimiter()
    return TestClient(app)
