from typing import Callable
from uuid import UUID

from src.app.ports.clock import Clock
from src.app.ports.open_banking_provider import OpenBankingProvider
from src.app.ports.token_generator import TokenGenerator
from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.connection_session import ConnectionSession


class StartBankConnection:
    def __init__(
        self,
        uow_factory: Callable[[], UnitOfWork],
        clock: Clock,
        provider: OpenBankingProvider,
        token_generator: TokenGenerator,
        session_lifetime_seconds: int,
    ) -> None:
        self._uow_factory = uow_factory
        self._clock = clock
        self._provider = provider
        self._token_generator = token_generator
        self._session_lifetime_seconds = session_lifetime_seconds

    async def __call__(
        self,
        user_id: UUID,
        institution_id: str,
        redirect_uri: str,
    ) -> ConnectionSession:
        reference = self._token_generator.generate()
        requisition = await self._provider.create_requisition(
            institution_id=institution_id,
            redirect_uri=redirect_uri,
            reference=reference,
        )

        now = self._clock.now()
        session = ConnectionSession.create(
            user_id=user_id,
            institution_id=institution_id,
            requisition_id=requisition.requisition_id,
            link=requisition.link,
            redirect_uri=redirect_uri,
            now=now,
            lifetime_seconds=self._session_lifetime_seconds,
        )

        async with self._uow_factory() as uow:
            await uow.connection_sessions.add(session)

        return session
