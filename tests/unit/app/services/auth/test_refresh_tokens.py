from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

import pytest

from src.app.services.auth.refresh_tokens import RefreshTokens
from src.app.services.auth.token_pair import TokenPair
from src.domain.entities.refresh_token import RefreshToken
from src.domain.exceptions.refresh_token_expired import RefreshTokenExpired
from src.domain.exceptions.refresh_token_not_found import RefreshTokenNotFound
from src.domain.exceptions.refresh_token_revoked import RefreshTokenRevoked
from tests.fakes.clock import FixedClock
from tests.fakes.jwt_issuer import StubJwtIssuer
from tests.fakes.repositories.refresh_token_repository import (
    InMemoryRefreshTokenRepository,
)
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.token_generator import StubTokenGenerator
from tests.fakes.unit_of_work import FakeUnitOfWork

NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
LIFETIME = 3600
NEW_RAW = "new-refresh-raw"
OLD_RAW = "old-refresh-raw"


class TestHappyPath:
    async def test_returns_token_pair_with_valid_access_for_user(self) -> None:
        user_id = uuid4()
        service, repo, jwt = _build_service()
        await _seed_active_token(repo, user_id=user_id, raw=OLD_RAW)

        pair = await service(OLD_RAW)

        assert isinstance(pair, TokenPair)
        assert pair.refresh == NEW_RAW
        assert jwt.verify(pair.access, NOW) == user_id

    async def test_old_token_is_revoked(self) -> None:
        service, repo, _ = _build_service()
        old = await _seed_active_token(repo, user_id=uuid4(), raw=OLD_RAW)

        await service(OLD_RAW)

        assert old.is_revoked is True
        assert old.revoked_at == NOW

    async def test_new_token_persisted_with_correct_shape(self) -> None:
        user_id = uuid4()
        service, repo, _ = _build_service()
        await _seed_active_token(repo, user_id=user_id, raw=OLD_RAW)

        await service(OLD_RAW)

        new = await repo.get_by_hash(RefreshToken.hash_raw(NEW_RAW))
        assert new is not None
        assert new.user_id == user_id
        assert new.expires_at == NOW + timedelta(seconds=LIFETIME)
        assert new.is_revoked is False


class TestNotFound:
    async def test_raises_when_hash_unknown(self) -> None:
        service, _, _ = _build_service()

        with pytest.raises(RefreshTokenNotFound):
            await service("anything")


class TestReuseAttack:
    async def test_raises_revoked_when_already_revoked(self) -> None:
        service, repo, _ = _build_service()
        await _seed_revoked_token(repo, user_id=uuid4(), raw=OLD_RAW)

        with pytest.raises(RefreshTokenRevoked):
            await service(OLD_RAW)

    async def test_revokes_all_user_tokens_on_reuse(self) -> None:
        user_id = uuid4()
        service, repo, _ = _build_service()
        await _seed_revoked_token(repo, user_id=user_id, raw=OLD_RAW)
        sibling = await _seed_active_token(repo, user_id=user_id, raw="sibling-raw")

        with pytest.raises(RefreshTokenRevoked):
            await service(OLD_RAW)

        assert sibling.is_revoked is True


class TestExpired:
    async def test_raises_expired_when_past_expiry(self) -> None:
        service, repo, _ = _build_service()
        await _seed_expired_token(repo, user_id=uuid4(), raw=OLD_RAW)

        with pytest.raises(RefreshTokenExpired):
            await service(OLD_RAW)

    async def test_does_not_revoke_sibling_tokens_on_expiry(self) -> None:
        user_id = uuid4()
        service, repo, _ = _build_service()
        await _seed_expired_token(repo, user_id=user_id, raw=OLD_RAW)
        sibling = await _seed_active_token(repo, user_id=user_id, raw="sibling-raw")

        with pytest.raises(RefreshTokenExpired):
            await service(OLD_RAW)

        assert sibling.is_revoked is False


def _build_service() -> tuple[RefreshTokens, InMemoryRefreshTokenRepository, StubJwtIssuer]:
    users = InMemoryUserRepository()
    refresh_tokens = InMemoryRefreshTokenRepository()
    uow = FakeUnitOfWork(users=users, refresh_tokens=refresh_tokens)
    jwt = StubJwtIssuer()
    service = RefreshTokens(
        uow_factory=lambda: uow,
        clock=FixedClock(NOW),
        jwt_issuer=jwt,
        token_generator=StubTokenGenerator(NEW_RAW),
        refresh_lifetime_seconds=LIFETIME,
    )
    return service, refresh_tokens, jwt


async def _seed_active_token(
    repo: InMemoryRefreshTokenRepository,
    user_id: UUID,
    raw: str,
) -> RefreshToken:
    token = RefreshToken.issue(
        user_id=user_id,
        token_hash=RefreshToken.hash_raw(raw),
        now=NOW,
        lifetime_seconds=LIFETIME,
    )
    await repo.add(token)
    return token


async def _seed_revoked_token(
    repo: InMemoryRefreshTokenRepository,
    user_id: UUID,
    raw: str,
) -> RefreshToken:
    token = await _seed_active_token(repo, user_id, raw)
    token.revoke(NOW - timedelta(minutes=5))
    return token


async def _seed_expired_token(
    repo: InMemoryRefreshTokenRepository,
    user_id: UUID,
    raw: str,
) -> RefreshToken:
    issued_at = NOW - timedelta(seconds=LIFETIME * 2)
    token = RefreshToken.issue(
        user_id=user_id,
        token_hash=RefreshToken.hash_raw(raw),
        now=issued_at,
        lifetime_seconds=LIFETIME,
    )
    await repo.add(token)
    return token
