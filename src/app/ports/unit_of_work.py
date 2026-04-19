from types import TracebackType
from typing import Protocol

from src.app.ports.repositories.account_repository import AccountRepository
from src.app.ports.repositories.balance_repository import BalanceRepository
from src.app.ports.repositories.connection_session_repository import ConnectionSessionRepository
from src.app.ports.repositories.fx_rate_repository import FxRateRepository
from src.app.ports.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.ports.repositories.transaction_repository import TransactionRepository
from src.app.ports.repositories.user_repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    refresh_tokens: RefreshTokenRepository
    accounts: AccountRepository
    connection_sessions: ConnectionSessionRepository
    transactions: TransactionRepository
    fx_rates: FxRateRepository
    balances: BalanceRepository

    async def __aenter__(self) -> "UnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
