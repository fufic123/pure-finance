"""account institution fk and balance_snapshots table

Revision ID: i9j0k1l2m3n4
Revises: h8i9j0k1l2m3
Create Date: 2026-04-21 14:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "i9j0k1l2m3n4"
down_revision: Union[str, None] = "h8i9j0k1l2m3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "accounts",
        sa.Column("institution_id", sa.UUID(), nullable=True),
    )
    op.create_foreign_key(
        "fk_accounts_institution_id",
        "accounts",
        "institutions",
        ["institution_id"],
        ["id"],
    )
    op.create_index("ix_accounts_institution_id", "accounts", ["institution_id"])

    op.add_column(
        "accounts",
        sa.Column(
            "balance",
            sa.Numeric(precision=16, scale=2),
            nullable=False,
            server_default="0",
        ),
    )

    op.create_table(
        "balance_snapshots",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("account_id", sa.UUID(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=16, scale=2), nullable=False),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_balance_snapshots_account_recorded_desc",
        "balance_snapshots",
        ["account_id", sa.text("recorded_at DESC")],
    )


def downgrade() -> None:
    op.drop_index("ix_balance_snapshots_account_recorded_desc", table_name="balance_snapshots")
    op.drop_table("balance_snapshots")

    op.drop_column("accounts", "balance")
    op.drop_index("ix_accounts_institution_id", table_name="accounts")
    op.drop_constraint("fk_accounts_institution_id", "accounts", type_="foreignkey")
    op.drop_column("accounts", "institution_id")
