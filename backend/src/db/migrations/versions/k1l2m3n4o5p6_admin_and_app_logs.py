"""add is_admin to users and create app_logs table

Revision ID: k1l2m3n4o5p6
Revises: j0k1l2m3n4o5
Create Date: 2026-04-26 14:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa

revision: str = "k1l2m3n4o5p6"
down_revision: Union[str, None] = "j0k1l2m3n4o5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op = sa.op if hasattr(sa, "op") else __import__("alembic.op", fromlist=["op"])

    import alembic.op as op

    op.add_column("users", sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False))

    op.create_table(
        "app_logs",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("level", sa.String(16), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("user_id", sa.UUID(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("traceback", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_app_logs_level_created_at", "app_logs", ["level", "created_at"])
    op.create_index("ix_app_logs_user_created_at", "app_logs", ["user_id", "created_at"])


def downgrade() -> None:
    import alembic.op as op

    op.drop_index("ix_app_logs_user_created_at", table_name="app_logs")
    op.drop_index("ix_app_logs_level_created_at", table_name="app_logs")
    op.drop_table("app_logs")
    op.drop_column("users", "is_admin")
