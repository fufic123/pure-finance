from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.integrations.auth.pyjwt_issuer import PyJwtIssuer

NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
LIFETIME = 3600
SECRET_A = "a" * 32
SECRET_B = "b" * 32


class TestIssueVerifyRoundtrip:
    def test_verify_returns_same_user_id_as_issued(self) -> None:
        issuer = PyJwtIssuer(secret=SECRET_A, lifetime_seconds=LIFETIME)
        user_id = uuid4()

        token = issuer.issue(user_id, NOW)

        assert issuer.verify(token, NOW) == user_id


class TestVerify:
    def test_raises_invalid_when_token_expired(self) -> None:
        issuer = PyJwtIssuer(secret=SECRET_A, lifetime_seconds=LIFETIME)
        token = issuer.issue(uuid4(), NOW)

        with pytest.raises(AccessTokenInvalid):
            issuer.verify(token, NOW + timedelta(seconds=LIFETIME + 1))

    def test_raises_invalid_for_different_secret(self) -> None:
        issuer_a = PyJwtIssuer(secret=SECRET_A, lifetime_seconds=LIFETIME)
        issuer_b = PyJwtIssuer(secret=SECRET_B, lifetime_seconds=LIFETIME)
        token = issuer_a.issue(uuid4(), NOW)

        with pytest.raises(AccessTokenInvalid):
            issuer_b.verify(token, NOW)

    def test_raises_invalid_for_garbage_token(self) -> None:
        issuer = PyJwtIssuer(secret=SECRET_A, lifetime_seconds=LIFETIME)

        with pytest.raises(AccessTokenInvalid):
            issuer.verify("not-a-jwt", NOW)
