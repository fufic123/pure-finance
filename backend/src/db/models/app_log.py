from datetime import datetime
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class AppLog(Base):
    __tablename__ = "app_logs"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    level: Mapped[str] = mapped_column(String(16))
    message: Mapped[str] = mapped_column(Text)
    user_id: Mapped[UUID | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    traceback: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime]

    __table_args__ = (
        Index("ix_app_logs_level_created_at", "level", "created_at"),
        Index("ix_app_logs_user_created_at", "user_id", "created_at"),
    )

    @classmethod
    def info(cls, message: str, now: datetime, user_id: UUID | None = None) -> "AppLog":
        return cls(id=uuid7(), level="INFO", message=message, user_id=user_id, created_at=now)

    @classmethod
    def error(cls, message: str, now: datetime, user_id: UUID | None = None, traceback: str | None = None) -> "AppLog":
        return cls(id=uuid7(), level="ERROR", message=message, user_id=user_id, traceback=traceback, created_at=now)
