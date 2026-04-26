from datetime import date
from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.transaction import Transaction


class PostgresTransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, transaction: Transaction) -> None:
        self._session.add(transaction)

    async def get_by_id(self, transaction_id: UUID) -> Transaction | None:
        result = await self._session.execute(select(Transaction).where(Transaction.id == transaction_id))
        return result.scalar_one_or_none()

    async def list_by_account(
        self,
        account_id: UUID,
        *,
        from_date: date | None = None,
        to_date: date | None = None,
        category_id: UUID | None = None,
    ) -> list[Transaction]:
        stmt = select(Transaction).where(Transaction.account_id == account_id)
        if from_date is not None:
            stmt = stmt.where(Transaction.booked_at >= from_date)
        if to_date is not None:
            stmt = stmt.where(Transaction.booked_at <= to_date)
        if category_id is not None:
            stmt = stmt.where(Transaction.category_id == category_id)
        result = await self._session.execute(stmt.order_by(Transaction.booked_at.desc()))
        return list(result.scalars().all())

    async def list_by_accounts(
        self,
        account_ids: list[UUID],
        *,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[Transaction]:
        if not account_ids:
            return []
        stmt = select(Transaction).where(Transaction.account_id.in_(account_ids))
        if from_date is not None:
            stmt = stmt.where(Transaction.booked_at >= from_date)
        if to_date is not None:
            stmt = stmt.where(Transaction.booked_at <= to_date)
        result = await self._session.execute(stmt.order_by(Transaction.booked_at.desc()))
        return list(result.scalars().all())

    async def list_all(self) -> list[Transaction]:
        result = await self._session.execute(select(Transaction).order_by(Transaction.booked_at.desc()))
        return list(result.scalars().all())

    async def update(self, transaction: Transaction) -> None:
        await self._session.merge(transaction)

    async def delete(self, transaction_id: UUID) -> None:
        await self._session.execute(delete(Transaction).where(Transaction.id == transaction_id))
