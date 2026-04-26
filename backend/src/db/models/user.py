from datetime import datetime
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    google_id: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(320))
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime]

    @classmethod
    def register(cls, google_id: str, email: str, now: datetime) -> "User":
        return cls(id=uuid7(), google_id=google_id, email=email, created_at=now, is_admin=False)
