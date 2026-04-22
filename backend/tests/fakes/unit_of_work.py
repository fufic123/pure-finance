from types import TracebackType

from src.app.ports.repositories.account_repository import AccountRepository
from src.app.ports.repositories.categorization_rule_repository import CategorizationRuleRepository
from src.app.ports.repositories.category_repository import CategoryRepository
from src.app.ports.repositories.refresh_token_repository import RefreshTokenRepository
from src.app.ports.repositories.transaction_repository import TransactionRepository
from src.app.ports.repositories.user_repository import UserRepository
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.categorization_rule_repository import InMemoryCategorizationRuleRepository
from tests.fakes.repositories.category_repository import InMemoryCategoryRepository
from tests.fakes.repositories.transaction_repository import InMemoryTransactionRepository


class FakeUnitOfWork:
    def __init__(
        self,
        users: UserRepository,
        refresh_tokens: RefreshTokenRepository,
        accounts: AccountRepository | None = None,
        transactions: TransactionRepository | None = None,
        categories: CategoryRepository | None = None,
        categorization_rules: CategorizationRuleRepository | None = None,
    ) -> None:
        self.users = users
        self.refresh_tokens = refresh_tokens
        self.accounts = accounts or InMemoryAccountRepository()
        self.transactions = transactions or InMemoryTransactionRepository()
        self.categories = categories or InMemoryCategoryRepository()
        self.categorization_rules = categorization_rules or InMemoryCategorizationRuleRepository()

    async def __aenter__(self) -> "FakeUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None
