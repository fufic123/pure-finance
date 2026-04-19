from urllib.parse import parse_qs, urlparse

from src.app.services.auth.start_google_auth import StartGoogleAuth
from tests.fakes.state_store import InMemoryStateStore
from tests.fakes.token_generator import StubTokenGenerator

CLIENT_ID = "test-client-id"
STATE = "generated-state-value"
REDIRECT_URI = "http://localhost:3000/callback"
STATE_LIFETIME = 600


class TestStartGoogleAuth:
    async def test_returns_google_authorization_url_with_expected_params(self) -> None:
        service, _ = _build_service()

        url = await service(REDIRECT_URI)

        parsed = urlparse(url)
        assert parsed.scheme == "https"
        assert parsed.netloc == "accounts.google.com"
        assert parsed.path == "/o/oauth2/v2/auth"

        params = parse_qs(parsed.query)
        assert params["client_id"] == [CLIENT_ID]
        assert params["redirect_uri"] == [REDIRECT_URI]
        assert params["response_type"] == ["code"]
        assert params["scope"] == ["openid email"]
        assert params["state"] == [STATE]

    async def test_saves_state_to_store(self) -> None:
        service, store = _build_service()

        await service(REDIRECT_URI)

        assert await store.consume(STATE) is True


def _build_service() -> tuple[StartGoogleAuth, InMemoryStateStore]:
    store = InMemoryStateStore()
    service = StartGoogleAuth(
        state_store=store,
        token_generator=StubTokenGenerator(STATE),
        client_id=CLIENT_ID,
        state_lifetime_seconds=STATE_LIFETIME,
    )
    return service, store
