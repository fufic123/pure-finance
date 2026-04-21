"""categories table

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-04-19 17:00:00.000000

"""
from datetime import UTC, datetime
from typing import Sequence, Union
from uuid import uuid4

import sqlalchemy as sa
from alembic import op

revision: str = "d4e5f6a7b8c9"
down_revision: Union[str, None] = "c3d4e5f6a7b8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_NOW = datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)

_SYSTEM_CATEGORIES = [
    # (id, name, parent_name)
    ("food-drink", "Food & Drink", None),
    ("transport", "Transport", None),
    ("shopping", "Shopping", None),
    ("health", "Health", None),
    ("entertainment", "Entertainment", None),
    ("bills-utilities", "Bills & Utilities", None),
    ("income", "Income", None),
    ("savings-investments", "Savings & Investments", None),
    ("other", "Other", None),
    # Sub-categories
    ("groceries", "Groceries", "food-drink"),
    ("restaurants", "Restaurants", "food-drink"),
    ("coffee", "Coffee", "food-drink"),
    ("public-transport", "Public Transport", "transport"),
    ("taxi", "Taxi & Ridesharing", "transport"),
    ("fuel", "Fuel", "transport"),
    ("salary", "Salary", "income"),
    ("freelance", "Freelance", "income"),
    ("rent", "Rent", "bills-utilities"),
    ("subscriptions", "Subscriptions", "bills-utilities"),
]


def upgrade() -> None:
    categories_table = op.create_table(
        "categories",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("parent_id", sa.UUID(), nullable=True),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("is_system", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_categories_user_id", "categories", ["user_id"])

    # Build id lookup
    id_map: dict[str, str] = {}
    for slug, name, _ in _SYSTEM_CATEGORIES:
        id_map[slug] = str(uuid4())

    # Insert top-level first, then children
    rows = []
    for slug, name, parent_slug in _SYSTEM_CATEGORIES:
        rows.append({
            "id": id_map[slug],
            "user_id": None,
            "parent_id": id_map[parent_slug] if parent_slug else None,
            "name": name,
            "is_system": True,
            "created_at": _NOW,
        })
    op.bulk_insert(categories_table, rows)

    # Add FK from transactions.category_id to categories.id
    op.create_foreign_key(
        "fk_transactions_category_id",
        "transactions",
        "categories",
        ["category_id"],
        ["id"],
        ondelete="SET NULL",
    )


def downgrade() -> None:
    op.drop_constraint("fk_transactions_category_id", "transactions", type_="foreignkey")
    op.drop_index("ix_categories_user_id", table_name="categories")
    op.drop_table("categories")
