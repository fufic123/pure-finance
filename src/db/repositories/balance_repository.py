from uuid import UUID

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.balance import BalanceModel
from src.domain.entities.balance import Balance


class PostgresBalanceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def upsert(self, balance: Balance) -> None:
        stmt = (
            insert(BalanceModel)
            .values(
                account_id=balance.account_id,
                amount=balance.amount,
                currency=balance.currency,
                updated_at=balance.updated_at,
            )
            .on_conflict_do_update(
                index_elements=["account_id"],
                set_={
                    "amount": balance.amount,
                    "currency": balance.currency,
                    "updated_at": balance.updated_at,
                },
            )
        )
        await self._session.execute(stmt)

    async def get_by_account(self, account_id: UUID) -> Balance | None:
        stmt = select(BalanceModel).where(BalanceModel.account_id == account_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        if model is None:
            return None
        return Balance(
            account_id=model.account_id,
            amount=model.amount,
            currency=model.currency,
            updated_at=model.updated_at,
        )
