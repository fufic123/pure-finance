from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.app.services.auth.revoke_all_sessions import RevokeAllSessions
from src.db.models.refresh_token import RefreshToken
from tests.fakes.clock import FixedClock
from tests.fakes.repositories.refresh_token_repository import (
    InMemoryRefreshTokenRepository,
)
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
LIFETIME = 3600


class TestRevokeAllSessions:
    async def test_revokes_all_active_tokens_for_user(self) -> None:
        user_id = uuid4()
        other_user = uuid4()
        service, repo = _build_service()
        mine_a = await _seed_active_token(repo, user_id=user_id, raw="a")
        mine_b = await _seed_active_token(repo, user_id=user_id, raw="b")
        other = await _seed_active_token(repo, user_id=other_user, raw="c")

        await service(user_id)

        assert mine_a.is_revoked is True
        assert mine_b.is_revoked is True
        assert other.is_revoked is False


def _build_service() -> tuple[RevokeAllSessions, InMemoryRefreshTokenRepository]:
    users = InMemoryUserRepository()
    refresh_tokens = InMemoryRefreshTokenRepository()
    uow = FakeUnitOfWork(users=users, refresh_tokens=refresh_tokens)
    service = RevokeAllSessions(uow_factory=lambda: uow, clock=FixedClock(NOW))
    return service, refresh_tokens


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
