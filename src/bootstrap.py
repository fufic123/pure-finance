import httpx
from redis.asyncio import Redis

from src.app.ports.rate_limiter import RateLimiter
from src.app.ports.unit_of_work import UnitOfWork
from src.app.services.auth.get_current_user import GetCurrentUser
from src.app.services.auth.google_callback import GoogleCallback
from src.app.services.auth.logout import Logout
from src.app.services.auth.refresh_tokens import RefreshTokens
from src.app.services.auth.revoke_all_sessions import RevokeAllSessions
from src.app.services.auth.start_google_auth import StartGoogleAuth
from src.app.services.banking.fetch_fx_rates import FetchFxRates
from src.app.services.categorization_rules.create_rule import CreateRule
from src.app.services.categorization_rules.delete_rule import DeleteRule
from src.app.services.categorization_rules.list_rules import ListRules
from src.app.services.categories.create_category import CreateCategory
from src.app.services.categories.delete_category import DeleteCategory
from src.app.services.categories.list_categories import ListCategories
from src.app.services.banking.finalize_bank_connection import FinalizeBankConnection
from src.app.services.banking.get_account import GetAccount
from src.app.services.banking.get_balance import GetBalance
from src.app.services.banking.list_accounts import ListAccounts
from src.app.services.banking.list_institutions import ListInstitutions
from src.app.services.banking.list_transactions import ListTransactions
from src.app.services.banking.start_bank_connection import StartBankConnection
from src.app.services.banking.sync_account_balance import SyncAccountBalance
from src.app.services.banking.sync_transactions import SyncTransactions
from src.db.session import create_engine, create_session_maker
from src.db.unit_of_work import SqlAlchemyUnitOfWork
from src.integrations.auth.google_oauth import GoogleOauthClient
from src.integrations.auth.pyjwt_issuer import PyJwtIssuer
from src.integrations.auth.secrets_token_generator import SecretsTokenGenerator
from src.integrations.banking.gocardless_client import GoCardlessClient
from src.integrations.fx.ecb import EcbFxRateProvider
from src.integrations.cache.redis_rate_limiter import RedisRateLimiter
from src.integrations.cache.redis_state_store import RedisStateStore
from src.integrations.clock import SystemClock
from src.shared.env import Settings


class AppContainer:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._engine = create_engine(settings.database_url)
        self._session_maker = create_session_maker(self._engine)
        self._http = httpx.AsyncClient()
        self._redis = Redis.from_url(settings.redis_url, decode_responses=True)
        self._clock = SystemClock()
        self._jwt = PyJwtIssuer(
            secret=settings.jwt_secret,
            lifetime_seconds=settings.access_token_lifetime_seconds,
        )
        self._oauth = GoogleOauthClient(
            client_id=settings.google_client_id,
            client_secret=settings.google_client_secret,
            http_client=self._http,
        )
        self._token_generator = SecretsTokenGenerator()
        self._state_store = RedisStateStore(self._redis)
        self._rate_limiter = RedisRateLimiter(self._redis)
        self._gocardless = GoCardlessClient(
            secret_id=settings.gocardless_secret_id,
            secret_key=settings.gocardless_secret_key,
            http_client=self._http,
            redis=self._redis,
        )

    def _uow_factory(self) -> UnitOfWork:
        return SqlAlchemyUnitOfWork(self._session_maker)

    def rate_limiter(self) -> RateLimiter:
        return self._rate_limiter

    def start_google_auth(self) -> StartGoogleAuth:
        return StartGoogleAuth(
            state_store=self._state_store,
            token_generator=self._token_generator,
            client_id=self._settings.google_client_id,
            state_lifetime_seconds=self._settings.oauth_state_lifetime_seconds,
        )

    def google_callback(self) -> GoogleCallback:
        return GoogleCallback(
            uow_factory=self._uow_factory,
            clock=self._clock,
            jwt_issuer=self._jwt,
            oauth_provider=self._oauth,
            state_store=self._state_store,
            token_generator=self._token_generator,
            refresh_lifetime_seconds=self._settings.refresh_token_lifetime_seconds,
        )

    def refresh_tokens(self) -> RefreshTokens:
        return RefreshTokens(
            uow_factory=self._uow_factory,
            clock=self._clock,
            jwt_issuer=self._jwt,
            token_generator=self._token_generator,
            refresh_lifetime_seconds=self._settings.refresh_token_lifetime_seconds,
        )

    def logout(self) -> Logout:
        return Logout(uow_factory=self._uow_factory, clock=self._clock)

    def get_current_user(self) -> GetCurrentUser:
        return GetCurrentUser(
            uow_factory=self._uow_factory,
            clock=self._clock,
            jwt_issuer=self._jwt,
        )

    def list_institutions(self) -> ListInstitutions:
        return ListInstitutions(provider=self._gocardless)

    def start_bank_connection(self) -> StartBankConnection:
        return StartBankConnection(
            uow_factory=self._uow_factory,
            clock=self._clock,
            provider=self._gocardless,
            token_generator=self._token_generator,
            session_lifetime_seconds=self._settings.bank_connection_session_lifetime_seconds,
        )

    def finalize_bank_connection(self) -> FinalizeBankConnection:
        return FinalizeBankConnection(
            uow_factory=self._uow_factory,
            clock=self._clock,
            provider=self._gocardless,
        )

    def get_account(self) -> GetAccount:
        return GetAccount(uow_factory=self._uow_factory)

    def list_accounts(self) -> ListAccounts:
        return ListAccounts(uow_factory=self._uow_factory)

    def get_balance(self) -> GetBalance:
        return GetBalance(uow_factory=self._uow_factory)

    def sync_account_balance(self) -> SyncAccountBalance:
        return SyncAccountBalance(
            uow_factory=self._uow_factory,
            clock=self._clock,
            provider=self._gocardless,
        )

    def list_rules(self) -> ListRules:
        return ListRules(uow_factory=self._uow_factory)

    def create_rule(self) -> CreateRule:
        return CreateRule(uow_factory=self._uow_factory, clock=self._clock)

    def delete_rule(self) -> DeleteRule:
        return DeleteRule(uow_factory=self._uow_factory)

    def list_categories(self) -> ListCategories:
        return ListCategories(uow_factory=self._uow_factory)

    def create_category(self) -> CreateCategory:
        return CreateCategory(uow_factory=self._uow_factory, clock=self._clock)

    def delete_category(self) -> DeleteCategory:
        return DeleteCategory(uow_factory=self._uow_factory)

    def fetch_fx_rates(self) -> FetchFxRates:
        return FetchFxRates(
            uow_factory=self._uow_factory,
            provider=EcbFxRateProvider(self._http),
        )

    def sync_transactions(self) -> SyncTransactions:
        return SyncTransactions(
            uow_factory=self._uow_factory,
            clock=self._clock,
            provider=self._gocardless,
        )

    def list_transactions(self) -> ListTransactions:
        return ListTransactions(uow_factory=self._uow_factory)

    def revoke_all_sessions(self) -> RevokeAllSessions:
        return RevokeAllSessions(
            uow_factory=self._uow_factory,
            clock=self._clock,
        )

    async def dispose(self) -> None:
        await self._http.aclose()
        await self._redis.aclose()
        await self._engine.dispose()
