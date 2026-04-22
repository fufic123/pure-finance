from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import (
    get_current_user,
    get_delete_account,
    get_get_account,
    get_list_accounts,
    get_list_transactions,
    get_update_transaction,
)
from src.api.dtos.account_response import AccountResponse
from src.api.dtos.transaction_response import TransactionResponse
from src.api.dtos.update_transaction_request import UpdateTransactionRequest
from src.app.services.banking.delete_account import DeleteAccount
from src.app.services.banking.get_account import GetAccount
from src.app.services.banking.list_accounts import ListAccounts
from src.app.services.banking.list_transactions import ListTransactions
from src.app.services.banking.update_transaction import UpdateTransaction
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


@router.delete("/accounts/{account_id}", status_code=204)
async def delete_account(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[DeleteAccount, Depends(get_delete_account)],
) -> None:
    await service(account_id=account_id, user_id=user.id)


@router.get("/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListTransactions, Depends(get_list_transactions)],
    account_id: Annotated[UUID, Query()],
    from_date: Annotated[date | None, Query(alias="from")] = None,
    to_date: Annotated[date | None, Query(alias="to")] = None,
    category_id: Annotated[UUID | None, Query()] = None,
) -> list[TransactionResponse]:
    transactions = await service(
        account_id=account_id,
        user_id=user.id,
        from_date=from_date,
        to_date=to_date,
        category_id=category_id,
    )
    return [TransactionResponse.from_transaction(t) for t in transactions]


@router.patch("/transactions/{transaction_id}", response_model=TransactionResponse)
async def update_transaction(
    transaction_id: UUID,
    body: UpdateTransactionRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[UpdateTransaction, Depends(get_update_transaction)],
) -> TransactionResponse:
    transaction = await service(
        transaction_id=transaction_id,
        user_id=user.id,
        note=body.note,
        note_provided="note" in body.model_fields_set,
        category_id=body.category_id,
        category_provided="category_id" in body.model_fields_set,
    )
    return TransactionResponse.from_transaction(transaction)
