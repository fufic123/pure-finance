from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.account import AccountModel
from src.domain.entities.account import Account


class PostgresAccountRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, account: Account) -> None:
        self._session.add(self._to_model(account))

    async def get_by_id(self, account_id: UUID) -> Account | None:
        model = await self._session.get(AccountModel, account_id)
        return self._to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[Account]:
        stmt = select(AccountModel).where(AccountModel.user_id == user_id)
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def list_all(self) -> list[Account]:
        stmt = select(AccountModel)
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def delete(self, account_id: UUID) -> None:
        await self._session.execute(
            delete(AccountModel).where(AccountModel.id == account_id)
        )

    @staticmethod
    def _to_entity(model: AccountModel) -> Account:
        return Account(
            id=model.id,
            user_id=model.user_id,
            iban=model.iban,
            currency=model.currency,
            name=model.name,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: Account) -> AccountModel:
        return AccountModel(
            id=entity.id,
            user_id=entity.user_id,
            iban=entity.iban,
            currency=entity.currency,
            name=entity.name,
            created_at=entity.created_at,
        )
