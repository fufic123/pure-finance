from uuid import UUID

from src.domain.entities.account import Account


class InMemoryAccountRepository:
    def __init__(self) -> None:
        self._by_id: dict[UUID, Account] = {}

    async def add(self, account: Account) -> None:
        self._by_id[account.id] = account

    async def get_by_id(self, account_id: UUID) -> Account | None:
        return self._by_id.get(account_id)

    async def get_by_external_id(self, external_id: str) -> Account | None:
        for account in self._by_id.values():
            if account.external_id == external_id:
                return account
        return None

    async def list_by_user(self, user_id: UUID) -> list[Account]:
        return [a for a in self._by_id.values() if a.user_id == user_id]

    async def list_all(self) -> list[Account]:
        return list(self._by_id.values())

    async def delete_by_connection_session(self, session_id: UUID) -> None:
        to_delete = [aid for aid, a in self._by_id.items() if a.connection_session_id == session_id]
        for aid in to_delete:
            del self._by_id[aid]
