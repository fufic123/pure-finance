from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated

import httpx
from fastapi import Depends, Header, Request
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.app.ports.rate_limiter import RateLimiter
from src.app.services.analytics.get_by_category import GetAnalyticsByCategory
from src.app.services.analytics.get_summary import GetAnalyticsSummary
from src.app.services.auth.get_current_user import GetCurrentUser
from src.app.services.auth.google_callback import GoogleCallback
from src.app.services.auth.logout import Logout
from src.app.services.auth.refresh_tokens import RefreshTokens
from src.app.services.auth.start_google_auth import StartGoogleAuth
from src.app.services.accounts.create_account import CreateAccount
from src.app.services.accounts.delete_account import DeleteAccount
from src.app.services.accounts.get_account import GetAccount
from src.app.services.accounts.get_account_balance import GetAccountBalance
from src.app.services.accounts.list_accounts import ListAccounts
from src.app.services.accounts.update_account import UpdateAccount
from src.app.services.transactions.create_transaction import CreateTransaction
from src.app.services.transactions.delete_transaction import DeleteTransaction
from src.app.services.transactions.list_transactions import ListTransactions
from src.app.services.transactions.update_transaction import UpdateTransaction
from src.app.services.categorization_rules.create_rule import CreateRule
from src.app.services.categorization_rules.delete_rule import DeleteRule
from src.app.services.categorization_rules.list_rules import ListRules
from src.app.services.categories.create_category import CreateCategory
from src.app.services.categories.delete_category import DeleteCategory
from src.app.services.categories.list_categories import ListCategories
from src.db.session import create_engine, create_session_maker
from src.db.unit_of_work import SqlAlchemyUnitOfWork
from src.db.models.user import User
from src.integrations.auth.google_oauth import GoogleOauthClient
from src.integrations.auth.pyjwt_issuer import PyJwtIssuer
from src.integrations.auth.secrets_token_generator import SecretsTokenGenerator
from src.integrations.cache.redis_rate_limiter import RedisRateLimiter
from src.integrations.cache.redis_state_store import RedisStateStore
from src.integrations.clock import SystemClock
from src.shared.env import Settings

AUTH_RATE_LIMIT = 30
AUTH_RATE_WINDOW_SECONDS = 60


@dataclass
class _S:
    settings: Settings
    engine: AsyncEngine
    session_maker: async_sessionmaker[AsyncSession]
    http: httpx.AsyncClient
    redis: Redis
    clock: SystemClock
    jwt: PyJwtIssuer
    oauth: GoogleOauthClient
    token_generator: SecretsTokenGenerator
    state_store: RedisStateStore
    rate_limiter: RedisRateLimiter


@lru_cache(maxsize=1)
def _s() -> _S:
    settings = Settings()
    engine = create_engine(settings.database_url)
    session_maker = create_session_maker(engine)
    http = httpx.AsyncClient()
    redis: Redis = Redis.from_url(settings.redis_url, decode_responses=True)
    clock = SystemClock()
    jwt = PyJwtIssuer(
        secret=settings.jwt_secret,
        lifetime_seconds=settings.access_token_lifetime_seconds,
    )
    oauth = GoogleOauthClient(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        http_client=http,
    )
    token_generator = SecretsTokenGenerator()
    state_store = RedisStateStore(redis)
    rate_limiter = RedisRateLimiter(redis)

    return _S(
        settings=settings, engine=engine, session_maker=session_maker,
        http=http, redis=redis, clock=clock, jwt=jwt, oauth=oauth,
        token_generator=token_generator, state_store=state_store,
        rate_limiter=rate_limiter,
    )


def _uow_factory() -> SqlAlchemyUnitOfWork:
    return SqlAlchemyUnitOfWork(_s().session_maker)


def get_rate_limiter() -> RateLimiter:
    return _s().rate_limiter


async def dispose() -> None:
    if _s.cache_info().currsize == 0:
        return
    s = _s()
    await s.http.aclose()
    await s.redis.aclose()
    await s.engine.dispose()


async def rate_limit_auth(
    request: Request,
    limiter: Annotated[RateLimiter, Depends(get_rate_limiter)],
) -> None:
    host = request.client.host if request.client else "unknown"
    key = f"auth:{host}:{request.url.path}"
    await limiter.hit(key, limit=AUTH_RATE_LIMIT, window_seconds=AUTH_RATE_WINDOW_SECONDS)


def get_start_google_auth() -> StartGoogleAuth:
    s = _s()
    return StartGoogleAuth(
        state_store=s.state_store,
        token_generator=s.token_generator,
        client_id=s.settings.google_client_id,
        state_lifetime_seconds=s.settings.oauth_state_lifetime_seconds,
    )


def get_google_callback() -> GoogleCallback:
    s = _s()
    return GoogleCallback(
        uow_factory=_uow_factory,
        clock=s.clock,
        jwt_issuer=s.jwt,
        oauth_provider=s.oauth,
        state_store=s.state_store,
        token_generator=s.token_generator,
        refresh_lifetime_seconds=s.settings.refresh_token_lifetime_seconds,
    )


def get_refresh_tokens() -> RefreshTokens:
    s = _s()
    return RefreshTokens(
        uow_factory=_uow_factory,
        clock=s.clock,
        jwt_issuer=s.jwt,
        token_generator=s.token_generator,
        refresh_lifetime_seconds=s.settings.refresh_token_lifetime_seconds,
    )


def get_logout() -> Logout:
    return Logout(uow_factory=_uow_factory, clock=_s().clock)


def get_current_user_service() -> GetCurrentUser:
    s = _s()
    return GetCurrentUser(uow_factory=_uow_factory, clock=s.clock, jwt_issuer=s.jwt)


def get_get_account() -> GetAccount:
    return GetAccount(uow_factory=_uow_factory)


def get_list_accounts() -> ListAccounts:
    return ListAccounts(uow_factory=_uow_factory)


def get_delete_account() -> DeleteAccount:
    return DeleteAccount(uow_factory=_uow_factory)


def get_create_account() -> CreateAccount:
    return CreateAccount(uow_factory=_uow_factory, clock=_s().clock)


def get_update_account() -> UpdateAccount:
    return UpdateAccount(uow_factory=_uow_factory)


def get_get_account_balance() -> GetAccountBalance:
    return GetAccountBalance(uow_factory=_uow_factory)


def get_list_transactions() -> ListTransactions:
    return ListTransactions(uow_factory=_uow_factory)


def get_update_transaction() -> UpdateTransaction:
    return UpdateTransaction(uow_factory=_uow_factory)


def get_create_transaction() -> CreateTransaction:
    return CreateTransaction(uow_factory=_uow_factory, clock=_s().clock)


def get_delete_transaction() -> DeleteTransaction:
    return DeleteTransaction(uow_factory=_uow_factory)


def get_analytics_summary() -> GetAnalyticsSummary:
    return GetAnalyticsSummary(uow_factory=_uow_factory)


def get_analytics_by_category() -> GetAnalyticsByCategory:
    return GetAnalyticsByCategory(uow_factory=_uow_factory)


def get_list_categories() -> ListCategories:
    return ListCategories(uow_factory=_uow_factory)


def get_create_category() -> CreateCategory:
    return CreateCategory(uow_factory=_uow_factory, clock=_s().clock)


def get_delete_category() -> DeleteCategory:
    return DeleteCategory(uow_factory=_uow_factory)


def get_list_rules() -> ListRules:
    return ListRules(uow_factory=_uow_factory)


def get_create_rule() -> CreateRule:
    return CreateRule(uow_factory=_uow_factory, clock=_s().clock)


def get_delete_rule() -> DeleteRule:
    return DeleteRule(uow_factory=_uow_factory)


async def get_current_user(
    authorization: Annotated[str | None, Header()] = None,
    service: Annotated[GetCurrentUser, Depends(get_current_user_service)] = None,
) -> User:
    if authorization is None or not authorization.startswith("Bearer "):
        raise AccessTokenInvalid()
    token = authorization.removeprefix("Bearer ")
    return await service(token)
