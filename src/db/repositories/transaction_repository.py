from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.transaction import TransactionModel
from src.domain.entities.transaction import Transaction


class PostgresTransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, transaction: Transaction) -> None:
        self._session.add(self._to_model(transaction))

    async def get_by_external_id(self, external_id: str) -> Transaction | None:
        stmt = select(TransactionModel).where(TransactionModel.external_id == external_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def list_by_account(self, account_id: UUID) -> list[Transaction]:
        stmt = (
            select(TransactionModel)
            .where(TransactionModel.account_id == account_id)
            .order_by(TransactionModel.booked_at.desc())
        )
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    @staticmethod
    def _to_entity(model: TransactionModel) -> Transaction:
        return Transaction(
            id=model.id,
            account_id=model.account_id,
            external_id=model.external_id,
            amount=model.amount,
            currency=model.currency,
            description=model.description,
            booked_at=model.booked_at,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: Transaction) -> TransactionModel:
        return TransactionModel(
            id=entity.id,
            account_id=entity.account_id,
            external_id=entity.external_id,
            amount=entity.amount,
            currency=entity.currency,
            description=entity.description,
            booked_at=entity.booked_at,
            created_at=entity.created_at,
        )
