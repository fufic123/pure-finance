from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import (
    get_current_user,
    get_delete_account,
    get_finalize_bank_connection,
    get_get_account,
    get_get_balance,
    get_list_accounts,
    get_list_connections,
    get_list_institutions,
    get_list_transactions,
    get_revoke_connection,
    get_start_bank_connection,
    get_sync_account_balance,
    get_sync_transactions,
    get_update_transaction,
)
from src.api.dtos.account_response import AccountResponse
from src.api.dtos.balance_response import BalanceResponse
from src.api.dtos.connection_response import ConnectionResponse
from src.api.dtos.institution_response import InstitutionResponse
from src.api.dtos.start_connection_request import StartConnectionRequest
from src.api.dtos.start_connection_response import StartConnectionResponse
from src.api.dtos.transaction_response import TransactionResponse
from src.api.dtos.update_transaction_request import UpdateTransactionRequest
from src.app.services.banking.delete_account import DeleteAccount
from src.app.services.banking.finalize_bank_connection import FinalizeBankConnection
from src.app.services.banking.get_account import GetAccount
from src.app.services.banking.get_balance import GetBalance
from src.app.services.banking.list_accounts import ListAccounts
from src.app.services.banking.list_connections import ListConnections
from src.app.services.banking.list_institutions import ListInstitutions
from src.app.services.banking.list_transactions import ListTransactions
from src.app.services.banking.revoke_connection import RevokeConnection
from src.app.services.banking.start_bank_connection import StartBankConnection
from src.app.services.banking.sync_account_balance import SyncAccountBalance
from src.app.services.banking.sync_transactions import SyncTransactions
from src.app.services.banking.update_transaction import UpdateTransaction
from src.domain.entities.user import User

router = APIRouter()


@router.get("/institutions", response_model=list[InstitutionResponse])
async def list_institutions(
    country: str,
    service: Annotated[ListInstitutions, Depends(get_list_institutions)],
) -> list[InstitutionResponse]:
    institutions = await service(country)
    return [InstitutionResponse.from_institution(i) for i in institutions]


@router.get("/connections", response_model=list[ConnectionResponse])
async def list_connections(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListConnections, Depends(get_list_connections)],
) -> list[ConnectionResponse]:
    sessions = await service(user.id)
    return [ConnectionResponse.from_session(s) for s in sessions]


@router.delete("/connections/{session_id}", status_code=204)
async def revoke_connection(
    session_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[RevokeConnection, Depends(get_revoke_connection)],
) -> None:
    await service(session_id=session_id, user_id=user.id)


@router.post("/connections", response_model=StartConnectionResponse, status_code=201)
async def start_connection(
    body: StartConnectionRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[StartBankConnection, Depends(get_start_bank_connection)],
) -> StartConnectionResponse:
    session = await service(
        user_id=user.id,
        institution_id=body.institution_id,
        redirect_uri=body.redirect_uri,
    )
    return StartConnectionResponse.from_session(session)


@router.post("/connections/{session_id}/completion", response_model=list[AccountResponse])
async def finalize_connection(
    session_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[FinalizeBankConnection, Depends(get_finalize_bank_connection)],
) -> list[AccountResponse]:
    accounts = await service(session_id=session_id, user_id=user.id)
    return [AccountResponse.from_account(a) for a in accounts]


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


@router.post("/accounts/{account_id}/sync", status_code=200)
async def sync_account(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    get_acct: Annotated[GetAccount, Depends(get_get_account)],
    sync: Annotated[SyncTransactions, Depends(get_sync_transactions)],
    sync_balance: Annotated[SyncAccountBalance, Depends(get_sync_account_balance)],
) -> dict:
    account = await get_acct(account_id=account_id, user_id=user.id)
    added = await sync(account_id=account.id, account_external_id=account.external_id, user_id=user.id)
    await sync_balance(account_id=account.id, account_external_id=account.external_id)
    return {"added": added}


@router.get("/accounts/{account_id}/balance", response_model=BalanceResponse | None)
async def get_account_balance(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[GetBalance, Depends(get_get_balance)],
) -> BalanceResponse | None:
    balance = await service(account_id=account_id, user_id=user.id)
    return BalanceResponse.from_balance(balance) if balance else None


@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListTransactions, Depends(get_list_transactions)],
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
