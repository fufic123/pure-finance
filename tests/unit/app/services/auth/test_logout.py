from datetime import UTC, datetime
from uuid import uuid4

from src.app.services.auth.logout import Logout
from src.domain.entities.refresh_token import RefreshToken
from tests.fakes.clock import FixedClock
from tests.fakes.repositories.refresh_token_repository import (
    InMemoryRefreshTokenRepository,
)
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
LIFETIME = 3600


class TestLogout:
    async def test_revokes_token_when_found(self) -> None:
        service, repo = _build_service()
        token = await _seed_active_token(repo, raw="abc")

        await service("abc")

        assert token.is_revoked is True
        assert token.revoked_at == NOW

    async def test_noop_when_token_unknown(self) -> None:
        service, _ = _build_service()

        await service("does-not-exist")

    async def test_idempotent_when_already_revoked(self) -> None:
        service, repo = _build_service()
        token = await _seed_active_token(repo, raw="abc")
        token.revoke(datetime(2026, 4, 18, tzinfo=UTC))
        first_revoked_at = token.revoked_at

        await service("abc")

        assert token.revoked_at == first_revoked_at


def _build_service() -> tuple[Logout, InMemoryRefreshTokenRepository]:
    users = InMemoryUserRepository()
    refresh_tokens = InMemoryRefreshTokenRepository()
    uow = FakeUnitOfWork(users=users, refresh_tokens=refresh_tokens)
    service = Logout(uow_factory=lambda: uow, clock=FixedClock(NOW))
    return service, refresh_tokens


async def _seed_active_token(
    repo: InMemoryRefreshTokenRepository,
    raw: str,
) -> RefreshToken:
    token = RefreshToken.issue(
        user_id=uuid4(),
        token_hash=RefreshToken.hash_raw(raw),
        now=NOW,
        lifetime_seconds=LIFETIME,
    )
    await repo.add(token)
    return token
