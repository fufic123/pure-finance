from datetime import datetime
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from src.api.dependencies import _uow_factory, _clock
from src.db.models.account import Account
from src.db.models.category import Category
from src.db.models.categorization_rule import CategorizationRule
from src.db.models.transaction import Transaction

router = APIRouter(prefix="/models", tags=["admin-models"])


# ── Accounts ──────────────────────────────────────────────────────────────────

class AccountIn(BaseModel):
    user_id: UUID
    name: str
    currency: str
    balance: Decimal = Decimal("0")
    iban: str | None = None


class AccountPatch(BaseModel):
    name: str | None = None
    balance: Decimal | None = None
    iban: str | None = None


@router.get("/accounts")
async def list_accounts() -> list[dict]:
    async with _uow_factory() as uow:
        return [_account_dict(a) for a in await uow.accounts.list_all()]


@router.post("/accounts", status_code=201)
async def create_account(body: AccountIn) -> dict:
    async with _uow_factory() as uow:
        account = Account.create(
            user_id=body.user_id, name=body.name, currency=body.currency,
            balance=body.balance, iban=body.iban, now=_clock().now(),
        )
        await uow.accounts.add(account)
    return _account_dict(account)


@router.patch("/accounts/{account_id}")
async def update_account(account_id: UUID, body: AccountPatch) -> dict:
    async with _uow_factory() as uow:
        account = await uow.accounts.get_by_id(account_id)
        if account is None:
            return JSONResponse(status_code=404, content={"message": "account not found"})
        if body.name is not None:
            account.rename(body.name)
        if body.balance is not None:
            account.update_balance(body.balance)
        if body.iban is not None:
            account.iban = body.iban
    return _account_dict(account)


@router.delete("/accounts/{account_id}", status_code=204)
async def delete_account(account_id: UUID) -> None:
    async with _uow_factory() as uow:
        await uow.accounts.delete(account_id)


def _account_dict(a: Account) -> dict:
    return {
        "id": str(a.id), "user_id": str(a.user_id), "name": a.name,
        "currency": a.currency, "balance": str(a.balance),
        "iban": a.iban, "created_at": a.created_at.isoformat(),
    }


# ── Transactions ───────────────────────────────────────────────────────────────

class TransactionIn(BaseModel):
    account_id: UUID
    amount: Decimal
    currency: str
    description: str
    booked_at: datetime
    category_id: UUID | None = None
    note: str | None = None


class TransactionPatch(BaseModel):
    category_id: UUID | None = None
    note: str | None = None
    description: str | None = None


@router.get("/transactions")
async def list_transactions(account_id: UUID | None = None) -> list[dict]:
    async with _uow_factory() as uow:
        if account_id is not None:
            txs = await uow.transactions.list_by_account(account_id)
        else:
            txs = await uow.transactions.list_all()
        return [_tx_dict(t) for t in txs]


@router.post("/transactions", status_code=201)
async def create_transaction(body: TransactionIn) -> dict:
    async with _uow_factory() as uow:
        tx = Transaction.create(
            account_id=body.account_id, amount=body.amount, currency=body.currency,
            description=body.description, booked_at=body.booked_at, now=_clock().now(),
        )
        if body.category_id is not None:
            tx.categorize(body.category_id, manually=True)
        if body.note is not None:
            tx.set_note(body.note)
        await uow.transactions.add(tx)
    return _tx_dict(tx)


@router.patch("/transactions/{transaction_id}")
async def update_transaction(transaction_id: UUID, body: TransactionPatch) -> dict:
    async with _uow_factory() as uow:
        tx = await uow.transactions.get_by_id(transaction_id)
        if tx is None:
            return JSONResponse(status_code=404, content={"message": "transaction not found"})
        if body.description is not None:
            tx.description = body.description
        if "category_id" in body.model_fields_set:
            tx.categorize(body.category_id, manually=True)
        if "note" in body.model_fields_set:
            tx.set_note(body.note)
    return _tx_dict(tx)


@router.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: UUID) -> None:
    async with _uow_factory() as uow:
        await uow.transactions.delete(transaction_id)


def _tx_dict(t: Transaction) -> dict:
    return {
        "id": str(t.id), "account_id": str(t.account_id), "amount": str(t.amount),
        "currency": t.currency, "description": t.description,
        "booked_at": t.booked_at.isoformat(), "category_id": str(t.category_id) if t.category_id else None,
        "note": t.note, "manually_categorized": t.manually_categorized,
        "created_at": t.created_at.isoformat(),
    }


# ── Categories ────────────────────────────────────────────────────────────────

class CategoryIn(BaseModel):
    name: str
    user_id: UUID | None = None
    is_system: bool = False
    parent_id: UUID | None = None


class CategoryPatch(BaseModel):
    name: str | None = None


@router.get("/categories")
async def list_categories() -> list[dict]:
    async with _uow_factory() as uow:
        return [_cat_dict(c) for c in await uow.categories.list_all()]


@router.post("/categories", status_code=201)
async def create_category(body: CategoryIn) -> dict:
    async with _uow_factory() as uow:
        now = _clock().now()
        if body.is_system:
            cat = Category(
                id=__import__("uuid_extensions").uuid7(),
                user_id=None, parent_id=body.parent_id,
                name=body.name, is_system=True, created_at=now,
            )
        else:
            if body.user_id is None:
                return JSONResponse(status_code=422, content={"message": "user_id required for non-system category"})
            cat = Category.create_user(
                user_id=body.user_id, name=body.name,
                parent_id=body.parent_id, now=now,
            )
        await uow.categories.add(cat)
    return _cat_dict(cat)


@router.patch("/categories/{category_id}")
async def update_category(category_id: UUID, body: CategoryPatch) -> dict:
    async with _uow_factory() as uow:
        cat = await uow.categories.get_by_id(category_id)
        if cat is None:
            return JSONResponse(status_code=404, content={"message": "category not found"})
        if body.name is not None:
            cat.name = body.name
    return _cat_dict(cat)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(category_id: UUID) -> None:
    async with _uow_factory() as uow:
        await uow.categories.delete(category_id)


def _cat_dict(c: Category) -> dict:
    return {
        "id": str(c.id), "name": c.name, "is_system": c.is_system,
        "user_id": str(c.user_id) if c.user_id else None,
        "parent_id": str(c.parent_id) if c.parent_id else None,
    }


# ── Categorization Rules ───────────────────────────────────────────────────────

class RuleIn(BaseModel):
    user_id: UUID
    keyword: str
    category_id: UUID


@router.get("/rules")
async def list_rules() -> list[dict]:
    async with _uow_factory() as uow:
        return [_rule_dict(r) for r in await uow.categorization_rules.list_all()]


@router.post("/rules", status_code=201)
async def create_rule(body: RuleIn) -> dict:
    async with _uow_factory() as uow:
        rule = CategorizationRule.create(
            user_id=body.user_id, keyword=body.keyword,
            category_id=body.category_id, now=_clock().now(),
        )
        await uow.categorization_rules.add(rule)
    return _rule_dict(rule)


@router.delete("/rules/{rule_id}", status_code=204)
async def delete_rule(rule_id: UUID) -> None:
    async with _uow_factory() as uow:
        await uow.categorization_rules.delete(rule_id)


def _rule_dict(r: CategorizationRule) -> dict:
    return {
        "id": str(r.id), "user_id": str(r.user_id),
        "keyword": r.keyword, "category_id": str(r.category_id),
        "created_at": r.created_at.isoformat(),
    }
