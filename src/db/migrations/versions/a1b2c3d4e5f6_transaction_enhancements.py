"""transaction enhancements

Revision ID: a1b2c3d4e5f6
Revises: 947fc0b5b08e
Create Date: 2026-04-19 14:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = "947fc0b5b08e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("transactions", sa.Column("eur_amount", sa.Numeric(precision=18, scale=4), nullable=True))
    op.add_column("transactions", sa.Column("category_id", sa.UUID(), nullable=True))
    op.add_column("transactions", sa.Column("note", sa.String(2048), nullable=True))
    op.add_column("transactions", sa.Column("manually_categorized", sa.Boolean(), nullable=False, server_default="false"))
    op.create_index("ix_transactions_category_id", "transactions", ["category_id"])


def downgrade() -> None:
    op.drop_index("ix_transactions_category_id", table_name="transactions")
    op.drop_column("transactions", "manually_categorized")
    op.drop_column("transactions", "note")
    op.drop_column("transactions", "category_id")
    op.drop_column("transactions", "eur_amount")
