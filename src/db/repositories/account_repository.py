from uuid import UUID

from sqlalchemy import select
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

    async def get_by_external_id(self, external_id: str) -> Account | None:
        stmt = select(AccountModel).where(AccountModel.external_id == external_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_user(self, user_id: UUID) -> list[Account]:
        stmt = select(AccountModel).where(AccountModel.user_id == user_id)
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def list_all(self) -> list[Account]:
        stmt = select(AccountModel)
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: AccountModel) -> Account:
        return Account(
            id=model.id,
            user_id=model.user_id,
            institution_external_id=model.institution_external_id,
            external_id=model.external_id,
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
            institution_external_id=entity.institution_external_id,
            external_id=entity.external_id,
            iban=entity.iban,
            currency=entity.currency,
            name=entity.name,
            created_at=entity.created_at,
        )
