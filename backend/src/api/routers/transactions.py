from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import (
    get_create_transaction,
    get_current_user,
    get_delete_transaction,
    get_list_transactions,
    get_update_transaction,
)
from src.api.dtos.create_transaction_request import CreateTransactionRequest
from src.api.dtos.transaction_response import TransactionResponse
from src.api.dtos.update_transaction_request import UpdateTransactionRequest
from src.app.services.transactions.create_transaction import CreateTransaction
from src.app.services.transactions.delete_transaction import DeleteTransaction
from src.app.services.transactions.list_transactions import ListTransactions
from src.app.services.transactions.update_transaction import UpdateTransaction
from src.domain.entities.user import User

router = APIRouter()


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


@router.post("/transactions", response_model=TransactionResponse, status_code=201)
async def create_transaction(
    body: CreateTransactionRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CreateTransaction, Depends(get_create_transaction)],
) -> TransactionResponse:
    transaction = await service(
        user_id=user.id,
        account_id=body.account_id,
        amount=body.amount,
        currency=body.currency,
        description=body.description,
        booked_at=body.booked_at,
        category_id=body.category_id,
        note=body.note,
    )
    return TransactionResponse.from_transaction(transaction)


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


@router.delete("/transactions/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[DeleteTransaction, Depends(get_delete_transaction)],
) -> None:
    await service(transaction_id=transaction_id, user_id=user.id)
