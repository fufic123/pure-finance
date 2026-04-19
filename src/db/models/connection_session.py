from datetime import datetime
from uuid import UUID

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.domain.enums.connection_status import ConnectionStatus


class ConnectionSessionModel(Base):
    __tablename__ = "connection_sessions"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    institution_id: Mapped[str] = mapped_column(String(256))
    requisition_id: Mapped[str] = mapped_column(String(256), unique=True, index=True)
    link: Mapped[str] = mapped_column(String(2048))
    redirect_uri: Mapped[str] = mapped_column(String(2048))
    status: Mapped[str] = mapped_column(String(32))
    expires_at: Mapped[datetime]
    created_at: Mapped[datetime]
