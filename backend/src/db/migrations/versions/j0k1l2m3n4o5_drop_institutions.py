"""drop institutions and institution_id from accounts

Revision ID: j0k1l2m3n4o5
Revises: i9j0k1l2m3n4
Create Date: 2026-04-26 12:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "j0k1l2m3n4o5"
down_revision: Union[str, None] = "i9j0k1l2m3n4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_index("ix_accounts_institution_id", table_name="accounts")
    op.drop_constraint("fk_accounts_institution_id", "accounts", type_="foreignkey")
    op.drop_column("accounts", "institution_id")
    op.drop_table("institutions")


def downgrade() -> None:
    op.create_table(
        "institutions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
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
