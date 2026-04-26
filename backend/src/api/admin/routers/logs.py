from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Query

from src.api.dependencies import _uow_factory

router = APIRouter(prefix="/logs", tags=["admin-logs"])


@router.get("")
async def list_logs(
    from_dt: datetime = Query(alias="from"),
    to_dt: datetime = Query(alias="to"),
    user_id: UUID | None = None,
    level: str | None = None,
) -> list[dict]:
    async with _uow_factory() as uow:
        logs = await uow.app_logs.list_by_period(from_dt, to_dt, level=level, user_id=user_id)
        return [
            {
                "id": str(log.id),
                "level": log.level,
                "message": log.message,
                "user_id": str(log.user_id) if log.user_id else None,
                "traceback": log.traceback,
                "created_at": log.created_at.isoformat(),
            }
            for log in logs
        ]


@router.get("/errors/count")
async def error_count(
    from_dt: datetime = Query(alias="from"),
    to_dt: datetime = Query(alias="to"),
) -> dict:
    async with _uow_factory() as uow:
        count = await uow.app_logs.count_by_period(from_dt, to_dt, level="ERROR")
        return {"from": from_dt.isoformat(), "to": to_dt.isoformat(), "error_count": count}
