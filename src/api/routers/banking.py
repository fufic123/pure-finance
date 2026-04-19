from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import (
    get_current_user,
    get_finalize_bank_connection,
    get_get_account,
    get_list_accounts,
    get_list_institutions,
    get_list_transactions,
    get_start_bank_connection,
    get_sync_transactions,
)
from src.api.dtos.account_response import AccountResponse
from src.api.dtos.institution_response import InstitutionResponse
from src.api.dtos.start_connection_request import StartConnectionRequest
from src.api.dtos.start_connection_response import StartConnectionResponse
from src.api.dtos.transaction_response import TransactionResponse
from src.app.services.banking.finalize_bank_connection import FinalizeBankConnection
from src.app.services.banking.list_accounts import ListAccounts
from src.app.services.banking.list_institutions import ListInstitutions
from src.app.services.banking.get_account import GetAccount
from src.app.services.banking.list_transactions import ListTransactions
from src.app.services.banking.start_bank_connection import StartBankConnection
from src.app.services.banking.sync_transactions import SyncTransactions
from src.domain.entities.user import User

router = APIRouter()


@router.get("/institutions", response_model=list[InstitutionResponse])
async def list_institutions(
    country: str,
    service: Annotated[ListInstitutions, Depends(get_list_institutions)],
) -> list[InstitutionResponse]:
    institutions = await service(country)
    return [InstitutionResponse.from_institution(i) for i in institutions]


@router.post("/connections/start", response_model=StartConnectionResponse)
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


@router.post("/connections/{session_id}/finalize", response_model=list[AccountResponse])
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


@router.post("/accounts/{account_id}/sync", status_code=200)
async def sync_account(
    account_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    get_acct: Annotated[GetAccount, Depends(get_get_account)],
    sync: Annotated[SyncTransactions, Depends(get_sync_transactions)],
) -> dict:
    account = await get_acct(account_id=account_id, user_id=user.id)
    added = await sync(account_id=account.id, account_external_id=account.external_id)
    return {"added": added}


@router.get("/accounts/{account_id}/transactions", response_model=list[TransactionResponse])
async def list_transactions(
    account_id: UUID,
    _: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListTransactions, Depends(get_list_transactions)],
) -> list[TransactionResponse]:
    transactions = await service(account_id=account_id, user_id=_.id)
    return [TransactionResponse.from_transaction(t) for t in transactions]
