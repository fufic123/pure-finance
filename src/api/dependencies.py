from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Header, Request

from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.app.ports.rate_limiter import RateLimiter
from src.app.services.auth.get_current_user import GetCurrentUser
from src.app.services.auth.google_callback import GoogleCallback
from src.app.services.auth.logout import Logout
from src.app.services.auth.refresh_tokens import RefreshTokens
from src.app.services.auth.start_google_auth import StartGoogleAuth
from src.app.services.banking.finalize_bank_connection import FinalizeBankConnection
from src.app.services.banking.get_account import GetAccount
from src.app.services.banking.get_balance import GetBalance
from src.app.services.banking.list_accounts import ListAccounts
from src.app.services.banking.list_institutions import ListInstitutions
from src.app.services.banking.list_transactions import ListTransactions
from src.app.services.banking.start_bank_connection import StartBankConnection
from src.app.services.banking.sync_account_balance import SyncAccountBalance
from src.app.services.banking.sync_transactions import SyncTransactions
from src.app.services.categorization_rules.create_rule import CreateRule
from src.app.services.categorization_rules.delete_rule import DeleteRule
from src.app.services.categorization_rules.list_rules import ListRules
from src.app.services.categories.create_category import CreateCategory
from src.app.services.categories.delete_category import DeleteCategory
from src.app.services.categories.list_categories import ListCategories
from src.bootstrap import AppContainer
from src.domain.entities.user import User
from src.shared.env import Settings

AUTH_RATE_LIMIT = 30
AUTH_RATE_WINDOW_SECONDS = 60


@lru_cache(maxsize=1)
def get_container() -> AppContainer:
    return AppContainer(Settings())


Container = Annotated[AppContainer, Depends(get_container)]


def get_rate_limiter(container: Container) -> RateLimiter:
    return container.rate_limiter()


async def rate_limit_auth(
    request: Request,
    limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
) -> None:
    host = request.client.host if request.client else "unknown"
    key = f"auth:{host}:{request.url.path}"
    await limiter.hit(key, limit=AUTH_RATE_LIMIT, window_seconds=AUTH_RATE_WINDOW_SECONDS)


def get_start_google_auth(container: Container) -> StartGoogleAuth:
    return container.start_google_auth()


def get_google_callback(container: Container) -> GoogleCallback:
    return container.google_callback()


def get_refresh_tokens(container: Container) -> RefreshTokens:
    return container.refresh_tokens()


def get_logout(container: Container) -> Logout:
    return container.logout()


def get_current_user_service(container: Container) -> GetCurrentUser:
    return container.get_current_user()


def get_list_institutions(container: Container) -> ListInstitutions:
    return container.list_institutions()


def get_start_bank_connection(container: Container) -> StartBankConnection:
    return container.start_bank_connection()


def get_finalize_bank_connection(container: Container) -> FinalizeBankConnection:
    return container.finalize_bank_connection()


def get_get_account(container: Container) -> GetAccount:
    return container.get_account()


def get_list_accounts(container: Container) -> ListAccounts:
    return container.list_accounts()


def get_list_transactions(container: Container) -> ListTransactions:
    return container.list_transactions()


def get_sync_transactions(container: Container) -> SyncTransactions:
    return container.sync_transactions()


def get_get_balance(container: Container) -> GetBalance:
    return container.get_balance()


def get_sync_account_balance(container: Container) -> SyncAccountBalance:
    return container.sync_account_balance()


def get_list_categories(container: Container) -> ListCategories:
    return container.list_categories()


def get_create_category(container: Container) -> CreateCategory:
    return container.create_category()


def get_delete_category(container: Container) -> DeleteCategory:
    return container.delete_category()


def get_list_rules(container: Container) -> ListRules:
    return container.list_rules()


def get_create_rule(container: Container) -> CreateRule:
    return container.create_rule()


def get_delete_rule(container: Container) -> DeleteRule:
    return container.delete_rule()


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    service: Annotated[GetCurrentUser, Depends(get_current_user_service)] = None,
) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise AccessTokenInvalid()
    token = authorization.removeprefix("Bearer ")
    return await service(token)
