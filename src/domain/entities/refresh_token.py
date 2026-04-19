import hashlib
from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import UUID, uuid4

from src.domain.exceptions.refresh_token_expired import RefreshTokenExpired
from src.domain.exceptions.refresh_token_revoked import RefreshTokenRevoked


@dataclass(slots=True)
class RefreshToken:
    id: UUID
    user_id: UUID
    token_hash: bytes
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None = None

    @classmethod
    def issue(
        cls,
        user_id: UUID,
        token_hash: bytes,
        now: datetime,
        lifetime_seconds: int,
    ) -> "RefreshToken":
        return cls(
            id=uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            created_at=now,
            expires_at=now + timedelta(seconds=lifetime_seconds),
        )

    @staticmethod
    def hash_raw(raw: str) -> bytes:
        return hashlib.sha256(raw.encode()).digest()

    @property
    def is_revoked(self) -> bool:
        return self.revoked_at is not None

    def is_expired(self, now: datetime) -> bool:
        return now >= self.expires_at

    def ensure_usable(self, now: datetime) -> None:
        if self.is_revoked:
            raise RefreshTokenRevoked(self.id)
        if self.is_expired(now):
            raise RefreshTokenExpired(self.id)

    def revoke(self, now: datetime) -> None:
        if self.is_revoked:
            return
        self.revoked_at = now
