from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, Index, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class RefreshTokenModel(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    token_hash: Mapped[bytes] = mapped_column(
        LargeBinary(32),
        unique=True,
        index=True,
    )
    created_at: Mapped[datetime]
    expires_at: Mapped[datetime]
    revoked_at: Mapped[datetime | None]

    __table_args__ = (
        Index(
            "ix_refresh_tokens_active_per_user",
            "user_id",
            postgresql_where="revoked_at IS NULL",
        ),
    )
