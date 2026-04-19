"""account connection_session_id and connection status REVOKED

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-04-19 19:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f6a7b8c9d0e1"
down_revision: Union[str, None] = "e5f6a7b8c9d0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "accounts",
        sa.Column(
            "connection_session_id",
            sa.UUID(),
            nullable=True,
        ),
    )
    op.create_foreign_key(
        "fk_accounts_connection_session_id",
        "accounts",
        "connection_sessions",
        ["connection_session_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_accounts_connection_session_id", "accounts", ["connection_session_id"])


def downgrade() -> None:
    op.drop_index("ix_accounts_connection_session_id", table_name="accounts")
    op.drop_constraint("fk_accounts_connection_session_id", "accounts", type_="foreignkey")
    op.drop_column("accounts", "connection_session_id")
