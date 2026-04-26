from datetime import datetime
from uuid import UUID
from uuid_extensions import uuid7

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class CategorizationRule(Base):
    __tablename__ = "categorization_rules"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(index=True)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    keyword: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime]

    @classmethod
    def create(cls, user_id: UUID, category_id: UUID, keyword: str, now: datetime) -> "CategorizationRule":
        return cls(id=uuid7(), user_id=user_id, category_id=category_id, keyword=keyword, created_at=now)

    def matches(self, description: str) -> bool:
        return self.keyword.lower() in description.lower()
