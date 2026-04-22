"""drop gocardless and fx integration

Revision ID: g7h8i9j0k1l2
Revises: f6a7b8c9d0e1
Create Date: 2026-04-21 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

revision: str = "g7h8i9j0k1l2"
down_revision: Union[str, None] = "f6a7b8c9d0e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # drop FK + index + column from accounts first (they reference connection_sessions)
    op.drop_index("ix_accounts_connection_session_id", table_name="accounts")
    op.drop_constraint("fk_accounts_connection_session_id", "accounts", type_="foreignkey")
    op.drop_column("accounts", "connection_session_id")

    op.drop_index("ix_accounts_institution_external_id", table_name="accounts")
    op.drop_column("accounts", "institution_external_id")

    op.drop_index("ix_accounts_external_id", table_name="accounts")
    op.drop_column("accounts", "external_id")

    # transactions: drop eur_amount + external_id unique index; make external_id nullable
    op.drop_column("transactions", "eur_amount")
    op.drop_index("ix_transactions_external_id", table_name="transactions")
    op.alter_column("transactions", "external_id", nullable=True)
    op.create_index("ix_transactions_external_id", "transactions", ["external_id"], unique=False)

    # drop dependent tables
    op.drop_table("balances")
    op.drop_table("fx_rates")
    op.drop_table("connection_sessions")


def downgrade() -> None:
    raise NotImplementedError("drop_gocardless_and_fx is one-way")
