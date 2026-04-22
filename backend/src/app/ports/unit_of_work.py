from types import TracebackType
from typing import Protocol

from src.app.ports.repositories.account_repository import AccountRepository
from src.app.ports.repositories.balance_snapshot_repository import BalanceSnapshotRepository
from src.app.ports.repositories.categorization_rule_repository import CategorizationRuleRepository
from src.app.ports.repositories.category_repository import CategoryRepository
from src.app.ports.repositories.institution_repository import InstitutionRepository
from src.app.ports.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.ports.repositories.transaction_repository import TransactionRepository
from src.app.ports.repositories.user_repository import UserRepository


class UnitOfWork(Protocol):
    users: UserRepository
    refresh_tokens: RefreshTokenRepository
    accounts: AccountRepository
    balance_snapshots: BalanceSnapshotRepository
    transactions: TransactionRepository
    categories: CategoryRepository
    categorization_rules: CategorizationRuleRepository
    institutions: InstitutionRepository

    async def __aenter__(self) -> "UnitOfWork": ...

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None: ...
