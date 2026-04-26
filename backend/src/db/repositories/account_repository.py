from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.account import Account


class PostgresAccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, account: Account) -> None:
        self._session.add(account)

    async def get_by_id(self, account_id: UUID) -> Account | None:
        return await self._session.get(Account, account_id)

    async def list_by_user(self, user_id: UUID) -> list[Account]:
        result = await self._session.execute(select(Account).where(Account.user_id == user_id))
        return list(result.scalars().all())

    async def list_all(self) -> list[Account]:
        result = await self._session.execute(select(Account))
        return list(result.scalars().all())

    async def update(self, account: Account) -> None:
        await self._session.merge(account)

    async def delete(self, account_id: UUID) -> None:
        await self._session.execute(delete(Account).where(Account.id == account_id))
