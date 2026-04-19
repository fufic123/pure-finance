from datetime import datetime
from uuid import UUID

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    google_id: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(320))
    created_at: Mapped[datetime]
