from datetime import UTC, datetime, timedelta
from hashlib import sha256
from uuid import uuid4

import pytest

from src.db.models.refresh_token import RefreshToken
from src.app.exceptions.refresh_token_expired import RefreshTokenExpired
from src.app.exceptions.refresh_token_revoked import RefreshTokenRevoked


class TestRevoke:
    def test_sets_revoked_at(self) -> None:
        token = _issue(now=datetime(2026, 4, 19, tzinfo=UTC))
        moment = datetime(2026, 4, 19, 12, 0, tzinfo=UTC)
        token.revoke(moment)
        assert token.revoked_at == moment
        assert token.is_revoked is True

    def test_second_revoke_keeps_first_timestamp(self) -> None:
        token = _issue(now=datetime(2026, 4, 19, tzinfo=UTC))
        first = datetime(2026, 4, 19, 12, 0, tzinfo=UTC)
        later = datetime(2026, 4, 19, 13, 0, tzinfo=UTC)
        token.revoke(first)
        token.revoke(later)
        assert token.revoked_at == first


class TestEnsureUsable:
    def test_raises_revoked_when_revoked(self) -> None:
        token = _issue(now=datetime(2026, 4, 19, tzinfo=UTC))
        token.revoke(datetime(2026, 4, 19, 12, 0, tzinfo=UTC))
        with pytest.raises(RefreshTokenRevoked):
            token.ensure_usable(datetime(2026, 4, 19, 13, 0, tzinfo=UTC))

    def test_raises_expired_when_now_past_expiry(self) -> None:
        now_issued = datetime(2026, 4, 19, 0, 0, tzinfo=UTC)
        token = _issue(now=now_issued, lifetime_seconds=3600)
        with pytest.raises(RefreshTokenExpired):
            token.ensure_usable(datetime(2026, 4, 19, 2, 0, tzinfo=UTC))

    def test_silent_when_active(self) -> None:
        now_issued = datetime(2026, 4, 19, 0, 0, tzinfo=UTC)
        token = _issue(now=now_issued, lifetime_seconds=3600)
        token.ensure_usable(datetime(2026, 4, 19, 0, 30, tzinfo=UTC))


def _hash() -> bytes:
    return sha256(b"raw").digest()


def _issue(now: datetime, lifetime_seconds: int = 3600) -> RefreshToken:
    return RefreshToken.issue(
        user_id=uuid4(),
        token_hash=_hash(),
        now=now,
        lifetime_seconds=lifetime_seconds,
    )
