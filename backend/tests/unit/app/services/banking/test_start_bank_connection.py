from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.app.dtos.requisition_info import RequisitionInfo
from src.app.services.banking.start_bank_connection import StartBankConnection
from src.domain.enums.connection_status import ConnectionStatus
from tests.fakes.clock import FixedClock
from tests.fakes.open_banking_provider import FakeOpenBankingProvider
from tests.fakes.repositories.connection_session_repository import InMemoryConnectionSessionRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.token_generator import StubTokenGenerator
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)


def _make_service(
    provider: FakeOpenBankingProvider | None = None,
    sessions: InMemoryConnectionSessionRepository | None = None,
) -> tuple[StartBankConnection, InMemoryConnectionSessionRepository]:
    sessions = sessions or InMemoryConnectionSessionRepository()
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        connection_sessions=sessions,
    )
    service = StartBankConnection(
        uow_factory=lambda: uow,
        clock=FixedClock(_NOW),
        provider=provider or FakeOpenBankingProvider(),
        token_generator=StubTokenGenerator("ref-tok"),
        session_lifetime_seconds=3600,
    )
    return service, sessions


class TestStartBankConnection:
    @pytest.mark.asyncio
    async def test_creates_session_with_created_status(self) -> None:
        provider = FakeOpenBankingProvider(
            requisition=RequisitionInfo(
                requisition_id="req-abc",
                link="https://ob.example.com/auth?id=req-abc",
            )
        )
        service, sessions = _make_service(provider=provider)
        user_id = uuid4()

        session = await service(
            user_id=user_id,
            institution_id="REVOLUT_LT",
            redirect_uri="http://localhost/callback",
        )

        assert session.status == ConnectionStatus.CREATED
        assert session.user_id == user_id
        assert session.institution_id == "REVOLUT_LT"
        assert session.requisition_id == "req-abc"
        assert session.link == "https://ob.example.com/auth?id=req-abc"
        assert session.redirect_uri == "http://localhost/callback"

    @pytest.mark.asyncio
    async def test_persists_session_in_repository(self) -> None:
        service, sessions = _make_service()
        user_id = uuid4()

        session = await service(
            user_id=user_id,
            institution_id="REVOLUT_LT",
            redirect_uri="http://localhost/callback",
        )

        stored = await sessions.get_by_id(session.id)
        assert stored is not None
        assert stored.id == session.id

    @pytest.mark.asyncio
    async def test_session_expires_after_lifetime(self) -> None:
        service, _ = _make_service()

        session = await service(
            user_id=uuid4(),
            institution_id="REVOLUT_LT",
            redirect_uri="http://localhost/callback",
        )

        from datetime import timedelta
        assert not session.is_expired(_NOW)
        assert session.is_expired(_NOW + timedelta(seconds=3601))
