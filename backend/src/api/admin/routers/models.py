from fastapi import APIRouter

from src.api.dependencies import _uow_factory

router = APIRouter(prefix="/models", tags=["admin-models"])


@router.get("/accounts")
async def list_accounts() -> list[dict]:
    async with _uow_factory() as uow:
        accounts = await uow.accounts.list_all()
        return [
            {
                "id": str(a.id), "user_id": str(a.user_id), "name": a.name,
                "currency": a.currency, "balance": str(a.balance), "iban": a.iban,
                "created_at": a.created_at.isoformat(),
            }
            for a in accounts
        ]


@router.get("/categories")
async def list_categories() -> list[dict]:
    async with _uow_factory() as uow:
        cats = await uow.categories.list_all()
        return [
            {"id": str(c.id), "user_id": str(c.user_id) if c.user_id else None,
             "name": c.name, "is_system": c.is_system}
            for c in cats
        ]


@router.get("/rules")
async def list_rules() -> list[dict]:
    async with _uow_factory() as uow:
        rules = await uow.categorization_rules.list_all()
        return [
            {"id": str(r.id), "user_id": str(r.user_id), "keyword": r.keyword,
             "category_id": str(r.category_id), "created_at": r.created_at.isoformat()}
            for r in rules
        ]
