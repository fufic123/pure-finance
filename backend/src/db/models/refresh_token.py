import hashlib
from datetime import datetime, timedelta
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy import ForeignKey, Index, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from src.app.exceptions.refresh_token_expired import RefreshTokenExpired
from src.app.exceptions.refresh_token_revoked import RefreshTokenRevoked
from src.db.base import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    token_hash: Mapped[bytes] = mapped_column(LargeBinary(32), unique=True, index=True)
    created_at: Mapped[datetime]
    expires_at: Mapped[datetime]
    revoked_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        Index("ix_refresh_tokens_active_per_user", "user_id", postgresql_where="revoked_at IS NULL"),
    )

    @classmethod
    def issue(cls, user_id: UUID, token_hash: bytes, now: datetime, lifetime_seconds: int) -> "RefreshToken":
        return cls(
            id=uuid7(),
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
