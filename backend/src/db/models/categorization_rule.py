from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


class CategorizationRuleModel(Base):
    __tablename__ = "categorization_rules"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(index=True)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id", ondelete="CASCADE"),
    )
    keyword: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[datetime]
