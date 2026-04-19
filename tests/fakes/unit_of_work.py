from types import TracebackType

from src.app.ports.repositories.account_repository import AccountRepository
from src.app.ports.repositories.balance_repository import BalanceRepository
from src.app.ports.repositories.category_repository import CategoryRepository
from src.app.ports.repositories.connection_session_repository import ConnectionSessionRepository
from src.app.ports.repositories.fx_rate_repository import FxRateRepository
from src.app.ports.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.ports.repositories.transaction_repository import TransactionRepository
from src.app.ports.repositories.user_repository import UserRepository
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.balance_repository import InMemoryBalanceRepository
from tests.fakes.repositories.category_repository import InMemoryCategoryRepository
from tests.fakes.repositories.connection_session_repository import InMemoryConnectionSessionRepository
from tests.fakes.repositories.fx_rate_repository import InMemoryFxRateRepository
from tests.fakes.repositories.transaction_repository import InMemoryTransactionRepository


class FakeUnitOfWork:
    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        accounts: AccountRepository | None = None,
        connection_sessions: ConnectionSessionRepository | None = None,
        transactions: TransactionRepository | None = None,
        fx_rates: FxRateRepository | None = None,
        balances: BalanceRepository | None = None,
        categories: CategoryRepository | None = None,
    ) -> None:
        self.users = users
        self.refresh_tokens = refresh_tokens
        self.accounts = accounts or InMemoryAccountRepository()
        self.connection_sessions = connection_sessions or InMemoryConnectionSessionRepository()
        self.transactions = transactions or InMemoryTransactionRepository()
        self.fx_rates = fx_rates or InMemoryFxRateRepository()
        self.balances = balances or InMemoryBalanceRepository()
        self.categories = categories or InMemoryCategoryRepository()

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None
