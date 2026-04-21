from datetime import UTC, datetime, timedelta

import pytest

from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid
from src.app.ports.google_user_info import GoogleUserInfo
from src.app.services.auth.google_callback import GoogleCallback
from src.app.services.auth.token_pair import TokenPair
from src.domain.entities.refresh_token import RefreshToken
from src.domain.entities.user import User
from tests.fakes.clock import FixedClock
from tests.fakes.jwt_issuer import StubJwtIssuer
from tests.fakes.oauth_provider import StubOauthProvider
from tests.fakes.repositories.refresh_token_repository import (
    InMemoryRefreshTokenRepository,
)
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.state_store import InMemoryStateStore
from tests.fakes.token_generator import StubTokenGenerator
from tests.fakes.unit_of_work import FakeUnitOfWork

NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
LIFETIME = 3600
NEW_REFRESH = "new-refresh"
CODE = "google-code"
REDIRECT = "http://localhost/callback"
STATE = "valid-state"
GOOGLE_ID = "gsub-1"
EMAIL = "m@example.com"


class TestNewUser:
    async def test_creates_user_when_google_id_unknown(self) -> None:
        service, users, _, _, store = _build_service()
        await store.save(STATE, 600)

        await service(code=CODE, redirect_uri=REDIRECT, state=STATE)

        created = await users.get_by_google_id(GOOGLE_ID)
        assert created is not None
        assert created.email == EMAIL
        assert len(users) == 1


class TestExistingUser:
    async def test_reuses_user_without_creating_duplicate(self) -> None:
        service, users, _, _, store = _build_service()
        existing = User.register(
            google_id=GOOGLE_ID,
            email=EMAIL,
            now=NOW - timedelta(days=1),
        )
        await users.add(existing)
        await store.save(STATE, 600)

        await service(code=CODE, redirect_uri=REDIRECT, state=STATE)

        assert len(users) == 1
        found = await users.get_by_google_id(GOOGLE_ID)
        assert found is not None
        assert found.id == existing.id


class TestTokenPair:
    async def test_returns_pair_with_access_valid_for_user(self) -> None:
        service, users, _, jwt, store = _build_service()
        await store.save(STATE, 600)

        pair = await service(code=CODE, redirect_uri=REDIRECT, state=STATE)

        user = await users.get_by_google_id(GOOGLE_ID)
        assert user is not None
        assert isinstance(pair, TokenPair)
        assert pair.refresh == NEW_REFRESH
        assert jwt.verify(pair.access, NOW) == user.id

    async def test_persists_refresh_token_for_user(self) -> None:
        service, users, refresh_tokens, _, store = _build_service()
        await store.save(STATE, 600)

        await service(code=CODE, redirect_uri=REDIRECT, state=STATE)

        user = await users.get_by_google_id(GOOGLE_ID)
        assert user is not None
        persisted = await refresh_tokens.get_by_hash(
            RefreshToken.hash_raw(NEW_REFRESH),
        )
        assert persisted is not None
        assert persisted.user_id == user.id
        assert persisted.expires_at == NOW + timedelta(seconds=LIFETIME)
        assert persisted.is_revoked is False


class TestStateVerification:
    async def test_raises_when_state_unknown(self) -> None:
        service, _, _, _, _ = _build_service()

        with pytest.raises(OAuthStateInvalid):
            await service(code=CODE, redirect_uri=REDIRECT, state="unknown-state")

    async def test_state_consumed_once(self) -> None:
        service, _, _, _, store = _build_service()
        await store.save(STATE, 600)

        await service(code=CODE, redirect_uri=REDIRECT, state=STATE)

        with pytest.raises(OAuthStateInvalid):
            await service(code=CODE, redirect_uri=REDIRECT, state=STATE)


def _build_service() -> tuple[
    GoogleCallback,
    InMemoryUserRepository,
    InMemoryRefreshTokenRepository,
    StubJwtIssuer,
    InMemoryStateStore,
]:
    users = InMemoryUserRepository()
    refresh_tokens = InMemoryRefreshTokenRepository()
    uow = FakeUnitOfWork(users=users, refresh_tokens=refresh_tokens)
    jwt = StubJwtIssuer()
    oauth = StubOauthProvider(GoogleUserInfo(google_id=GOOGLE_ID, email=EMAIL))
    state_store = InMemoryStateStore()
    service = GoogleCallback(
        uow_factory=lambda: uow,
        clock=FixedClock(NOW),
        jwt_issuer=jwt,
        oauth_provider=oauth,
        state_store=state_store,
        token_generator=StubTokenGenerator(NEW_REFRESH),
        refresh_lifetime_seconds=LIFETIME,
    )
    return service, users, refresh_tokens, jwt, state_store
