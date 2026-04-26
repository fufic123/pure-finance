from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.api.dependencies import _uow_factory
from src.db.models.user import User

router = APIRouter(prefix="/users", tags=["admin-users"])


@router.get("")
async def list_users() -> list[dict]:
    async with _uow_factory() as uow:
        result = await uow.users.list_all()
        return [
            {"id": str(u.id), "email": u.email, "is_admin": u.is_admin, "created_at": u.created_at.isoformat()}
            for u in result
        ]


@router.get("/{user_id}")
async def get_user(user_id: UUID) -> dict:
    async with _uow_factory() as uow:
        user = await uow.users.get_by_id(user_id)
        if user is None:
            return JSONResponse(status_code=404, content={"message": "user not found"})
        accounts = await uow.accounts.list_by_user(user_id)
        return {
            "id": str(user.id),
            "email": user.email,
            "is_admin": user.is_admin,
            "created_at": user.created_at.isoformat(),
            "accounts": [
                {"id": str(a.id), "name": a.name, "currency": a.currency, "balance": str(a.balance)}
                for a in accounts
            ],
        }


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: UUID) -> None:
    async with _uow_factory() as uow:
        user = await uow.users.get_by_id(user_id)
        if user is not None:
            await uow.users.delete(user_id)


@router.patch("/{user_id}/toggle-admin", status_code=200)
async def toggle_admin(user_id: UUID) -> dict:
    async with _uow_factory() as uow:
        user = await uow.users.get_by_id(user_id)
        if user is None:
            return JSONResponse(status_code=404, content={"message": "user not found"})
        user.is_admin = not user.is_admin
        return {"id": str(user.id), "is_admin": user.is_admin}
