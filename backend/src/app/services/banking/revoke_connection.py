from typing import Callable
from uuid import UUID

from src.app.exceptions.connection_session_not_found import ConnectionSessionNotFound
from src.app.ports.open_banking_provider import OpenBankingProvider
from src.app.ports.unit_of_work import UnitOfWork


class RevokeConnection:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        provider: OpenBankingProvider,
    ) -> None:
        self._uow_factory = uow_factory
        self._provider = provider

    async def __call__(self, session_id: UUID, user_id: UUID) -> None:
        async with self._uow_factory() as uow:
            session = await uow.connection_sessions.get_by_id(session_id)
            if session is None or session.user_id != user_id:
                raise ConnectionSessionNotFound()
            await self._provider.revoke_requisition(session.requisition_id)
            await uow.accounts.delete_by_connection_session(session_id)
            session.mark_revoked()
            await uow.connection_sessions.update_status(session)
