from datetime import UTC, datetime

import pytest

from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.app.services.auth.get_current_user import GetCurrentUser
from src.domain.entities.user import User
from src.domain.exceptions.user_not_found import UserNotFound
from tests.fakes.clock import FixedClock
from tests.fakes.jwt_issuer import StubJwtIssuer
from tests.fakes.repositories.refresh_token_repository import (
    InMemoryRefreshTokenRepository,
)
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)


class TestGetCurrentUser:
    async def test_returns_user_when_token_valid(self) -> None:
        user = User.register(google_id="gsub-1", email="m@example.com", now=NOW)
        service, users, jwt = _build_service()
        await users.add(user)
        token = jwt.issue(user.id, NOW)

        result = await service(token)

        assert result.id == user.id
        assert result.email == user.email

    async def test_raises_access_token_invalid_for_unknown_token(self) -> None:
        service, _, _ = _build_service()

        with pytest.raises(AccessTokenInvalid):
            await service("garbage")

    async def test_raises_user_not_found_when_user_missing(self) -> None:
        user = User.register(google_id="gsub-1", email="m@example.com", now=NOW)
        service, _, jwt = _build_service()
        token = jwt.issue(user.id, NOW)

        with pytest.raises(UserNotFound):
            await service(token)


def _build_service() -> tuple[GetCurrentUser, InMemoryUserRepository, StubJwtIssuer]:
    users = InMemoryUserRepository()
    refresh_tokens = InMemoryRefreshTokenRepository()
    uow = FakeUnitOfWork(users=users, refresh_tokens=refresh_tokens)
    jwt = StubJwtIssuer()
    service = GetCurrentUser(
        uow_factory=lambda: uow,
        clock=FixedClock(NOW),
        jwt_issuer=jwt,
    )
    return service, users, jwt
