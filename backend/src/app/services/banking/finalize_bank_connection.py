from typing import Callable
from uuid import UUID

from src.app.exceptions.connection_session_expired import ConnectionSessionExpired
from src.app.exceptions.connection_session_not_found import ConnectionSessionNotFound
from src.app.ports.clock import Clock
from src.app.ports.open_banking_provider import OpenBankingProvider
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.account import Account
from src.domain.entities.connection_session import ConnectionSession


class FinalizeBankConnection:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        provider: OpenBankingProvider,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._provider = provider

    async def __call__(self, session_id: UUID, user_id: UUID) -> list[Account]:
        now = self._clock.now()

        async with self._uow_factory() as uow:
            session = await uow.connection_sessions.get_by_id(session_id)
            if session is None or session.user_id != user_id:
                raise ConnectionSessionNotFound()
            if session.is_expired(now):
                session.mark_expired()
                raise ConnectionSessionExpired()

            account_infos = await self._provider.list_accounts(session.requisition_id)

            accounts: list[Account] = []
            for info in account_infos:
                existing = await uow.accounts.get_by_external_id(info.external_id)
                if existing is not None:
                    accounts.append(existing)
                    continue
                account = Account.create(
                    user_id=user_id,
                    connection_session_id=session.id,
                    institution_external_id=session.institution_id,
                    external_id=info.external_id,
                    iban=info.iban,
                    currency=info.currency,
                    name=info.name,
                    now=now,
                )
                await uow.accounts.add(account)
                accounts.append(account)

            session.mark_linked()

        return accounts
