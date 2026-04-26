from fastapi import Request
from fastapi.responses import JSONResponse

from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.cannot_delete_system_category import CannotDeleteSystemCategory
from src.app.exceptions.category_not_found import CategoryNotFound
from src.app.exceptions.institution_not_found import InstitutionNotFound
from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid
from src.app.exceptions.rate_limit_exceeded import RateLimitExceeded
from src.app.exceptions.rule_not_found import RuleNotFound
from src.app.exceptions.transaction_not_found import TransactionNotFound


async def handle_access_token_invalid(request: Request, exc: AccessTokenInvalid) -> JSONResponse:
    return JSONResponse(status_code=401, content={"message": str(exc)})


async def handle_account_not_found(request: Request, exc: AccountNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "account not found"})


async def handle_cannot_delete_system_category(request: Request, exc: CannotDeleteSystemCategory) -> JSONResponse:
    return JSONResponse(status_code=403, content={"message": "cannot delete system category"})


async def handle_category_not_found(request: Request, exc: CategoryNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "category not found"})


async def handle_institution_not_found(request: Request, exc: InstitutionNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "institution not found"})


async def handle_oauth_state_invalid(request: Request, exc: OAuthStateInvalid) -> JSONResponse:
    return JSONResponse(status_code=400, content={"message": str(exc)})


async def handle_rate_limit_exceeded(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(status_code=429, content={"message": str(exc)})


async def handle_rule_not_found(request: Request, exc: RuleNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "rule not found"})


async def handle_transaction_not_found(request: Request, exc: TransactionNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"message": "transaction not found"})
