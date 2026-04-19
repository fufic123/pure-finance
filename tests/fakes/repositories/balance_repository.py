from uuid import UUID

from src.domain.entities.balance import Balance


class InMemoryBalanceRepository:
    def __init__(self) -> None:
        self._by_account: dict[UUID, Balance] = {}

    async def upsert(self, balance: Balance) -> None:
        self._by_account[balance.account_id] = balance

    async def get_by_account(self, account_id: UUID) -> Balance | None:
        return self._by_account.get(account_id)
