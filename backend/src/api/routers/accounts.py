from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.dependencies import (
    get_create_account,
    get_current_user,
    get_delete_account,
    get_get_account,
    get_get_account_balance,
    get_list_accounts,
    get_update_account,
)
from src.api.dtos.accounts.balance_response import BalanceResponse
from src.api.dtos.accounts.create_request import CreateAccountRequest
from src.api.dtos.accounts.response import AccountResponse
from src.api.dtos.accounts.update_request import UpdateAccountRequest
from src.app.services.accounts.create_account import CreateAccount
from src.app.services.accounts.delete_account import DeleteAccount
from src.app.services.accounts.get_account import GetAccount
from src.app.services.accounts.get_account_balance import GetAccountBalance
from src.app.services.accounts.list_accounts import ListAccounts
from src.app.services.accounts.update_account import UpdateAccount
from src.domain.entities.user import User

router = APIRouter()


@router.get("/accounts/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[GetAccount, Depends(get_get_account)],
) -> AccountResponse:
    account = await service(account_id=account_id, user_id=user.id)
    return AccountResponse.from_account(account)


@router.get("/accounts", response_model=list[AccountResponse])
async def list_accounts(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListAccounts, Depends(get_list_accounts)],
) -> list[AccountResponse]:
    accounts = await service(user.id)
    return [AccountResponse.from_account(a) for a in accounts]


@router.post("/accounts", response_model=AccountResponse, status_code=201)
async def create_account(
    body: CreateAccountRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CreateAccount, Depends(get_create_account)],
) -> AccountResponse:
    account = await service(
        user_id=user.id,
        institution_id=body.institution_id,
        name=body.name,
        currency=body.currency,
        balance=body.balance,
    )
    return AccountResponse.from_account(account)


@router.patch("/accounts/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: UUID,
    body: UpdateAccountRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UpdateAccount, Depends(get_update_account)],
) -> AccountResponse:
    account = await service(
        account_id=account_id,
        user_id=user.id,
        name=body.name,
        balance=body.balance,
        name_provided="name" in body.model_fields_set,
        balance_provided="balance" in body.model_fields_set,
    )
    return AccountResponse.from_account(account)


@router.delete("/accounts/{account_id}", status_code=204)
async def delete_account(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[DeleteAccount, Depends(get_delete_account)],
) -> None:
    await service(account_id=account_id, user_id=user.id)


@router.get("/accounts/{account_id}/balance", response_model=BalanceResponse)
async def get_account_balance(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[GetAccountBalance, Depends(get_get_account_balance)],
) -> BalanceResponse:
    balance = await service(account_id=account_id, user_id=user.id)
    if balance is None:
        raise HTTPException(status_code=404, detail="balance not found")
    return BalanceResponse(
        amount=balance.amount,
        currency=balance.currency,
        updated_at=balance.updated_at,
    )
