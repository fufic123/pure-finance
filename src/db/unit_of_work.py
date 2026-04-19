from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.app.ports.repositories.account_repository import AccountRepository
from src.app.ports.repositories.balance_repository import BalanceRepository
from src.app.ports.repositories.category_repository import CategoryRepository
from src.app.ports.repositories.connection_session_repository import ConnectionSessionRepository
from src.app.ports.repositories.fx_rate_repository import FxRateRepository
from src.app.ports.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.ports.repositories.transaction_repository import TransactionRepository
from src.app.ports.repositories.user_repository import UserRepository
from src.db.repositories.account_repository import PostgresAccountRepository
from src.db.repositories.balance_repository import PostgresBalanceRepository
from src.db.repositories.category_repository import PostgresCategoryRepository
from src.db.repositories.connection_session_repository import PostgresConnectionSessionRepository
from src.db.repositories.fx_rate_repository import PostgresFxRateRepository
from src.db.repositories.refresh_token_repository import PostgresRefreshTokenRepository
from src.db.repositories.transaction_repository import PostgresTransactionRepository
from src.db.repositories.user_repository import PostgresUserRepository


class SqlAlchemyUnitOfWork:
    users: UserRepository
    refresh_tokens: RefreshTokenRepository
    accounts: AccountRepository
    connection_sessions: ConnectionSessionRepository
    transactions: TransactionRepository
    fx_rates: FxRateRepository
    balances: BalanceRepository
    categories: CategoryRepository

    def __init__(self, session_maker: async_sessionmaker[AsyncSession]) -> None:
        self._session_maker = session_maker
        self._session: AsyncSession | None = None

    async def __aenter__(self) -> "SqlAlchemyUnitOfWork":
        self._session = self._session_maker()
        self.users = PostgresUserRepository(self._session)
        self.refresh_tokens = PostgresRefreshTokenRepository(self._session)
        self.accounts = PostgresAccountRepository(self._session)
        self.connection_sessions = PostgresConnectionSessionRepository(self._session)
        self.transactions = PostgresTransactionRepository(self._session)
        self.fx_rates = PostgresFxRateRepository(self._session)
        self.balances = PostgresBalanceRepository(self._session)
        self.categories = PostgresCategoryRepository(self._session)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        assert self._session is not None
        try:
            if exc_type is None:
                await self._session.commit()
            else:
                await self._session.rollback()
        finally:
            await self._session.close()
            self._session = None
