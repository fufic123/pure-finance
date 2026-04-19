from datetime import datetime
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID | None] = mapped_column(nullable=True, index=True)
    parent_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(100))
    is_system: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    created_at: Mapped[datetime]
