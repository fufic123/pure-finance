"""institutions table with seed

Revision ID: h8i9j0k1l2m3
Revises: g7h8i9j0k1l2
Create Date: 2026-04-21 13:00:00.000000

"""
from datetime import UTC, datetime
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision: str = "h8i9j0k1l2m3"
down_revision: Union[str, None] = "g7h8i9j0k1l2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_NOW = datetime(2026, 4, 21, 0, 0, 0, tzinfo=UTC)

_SEED_NAMES = [
    "SEB",
    "Swedbank",
    "Luminor",
    "LHV",
    "Citadele",
    "Revolut",
    "Paysera",
    "Šiaulių bankas",
    "Monobank",
    "PrivatBank",
    "Wise",
    "N26",
    "Other",
]


def upgrade() -> None:
    institutions_table = op.create_table(
        "institutions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(80), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_institutions_name"),
    )
    rows = [{"id": str(uuid4()), "name": name, "created_at": _NOW} for name in _SEED_NAMES]
    op.bulk_insert(institutions_table, rows)


def downgrade() -> None:
    op.drop_table("institutions")
