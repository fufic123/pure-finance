from datetime import datetime

from fastapi import APIRouter, Query
from sqlalchemy import func, select

from src.api.dependencies import _session_maker
from src.db.models.account import Account
from src.db.models.transaction import Transaction
from src.db.models.user import User

router = APIRouter(prefix="/stats", tags=["admin-stats"])


@router.get("")
async def get_stats(
    from_dt: datetime = Query(alias="from"),
    to_dt: datetime = Query(alias="to"),
) -> dict:
    async with _session_maker()() as session:
        total_users = (await session.execute(select(func.count()).select_from(User))).scalar_one()
        new_users = (await session.execute(
            select(func.count()).select_from(User).where(User.created_at >= from_dt, User.created_at <= to_dt)
        )).scalar_one()
        total_accounts = (await session.execute(select(func.count()).select_from(Account))).scalar_one()
        tx_count = (await session.execute(
            select(func.count()).select_from(Transaction).where(
                Transaction.created_at >= from_dt, Transaction.created_at <= to_dt
            )
        )).scalar_one()
        tx_volume = (await session.execute(
            select(func.sum(Transaction.amount)).where(
                Transaction.created_at >= from_dt, Transaction.created_at <= to_dt
            )
        )).scalar_one()

    return {
        "period": {"from": from_dt.isoformat(), "to": to_dt.isoformat()},
        "users": {"total": total_users, "new_in_period": new_users},
        "accounts": {"total": total_accounts},
        "transactions": {"count": tx_count, "volume": str(tx_volume or 0)},
    }
