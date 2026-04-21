from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest

from src.app.dtos.bank_account_info import BankAccountInfo
from src.app.exceptions.connection_session_expired import ConnectionSessionExpired
from src.app.exceptions.connection_session_not_found import ConnectionSessionNotFound
from src.app.services.banking.finalize_bank_connection import FinalizeBankConnection
from src.domain.entities.connection_session import ConnectionSession
from src.domain.enums.connection_status import ConnectionStatus
from tests.fakes.clock import FixedClock
from tests.fakes.open_banking_provider import FakeOpenBankingProvider
from tests.fakes.repositories.account_repository import InMemoryAccountRepository
from tests.fakes.repositories.connection_session_repository import InMemoryConnectionSessionRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)


def _make_session(
    user_id=None,
    expires_at: datetime | None = None,
) -> ConnectionSession:
    return ConnectionSession(
        id=uuid4(),
        user_id=user_id or uuid4(),
        institution_id="REVOLUT_LT",
        requisition_id="req-abc",
        link="https://ob.example.com/auth",
        redirect_uri="http://localhost/callback",
        status=ConnectionStatus.CREATED,
        expires_at=expires_at or (_NOW + timedelta(hours=1)),
        created_at=_NOW,
    )


def _make_service(
    provider: FakeOpenBankingProvider | None = None,
    sessions: InMemoryConnectionSessionRepository | None = None,
    accounts: InMemoryAccountRepository | None = None,
) -> tuple[FinalizeBankConnection, InMemoryConnectionSessionRepository, InMemoryAccountRepository]:
    sessions = sessions or InMemoryConnectionSessionRepository()
    accounts = accounts or InMemoryAccountRepository()
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        accounts=accounts,
        connection_sessions=sessions,
    )
    service = FinalizeBankConnection(
        uow_factory=lambda: uow,
        clock=FixedClock(_NOW),
        provider=provider or FakeOpenBankingProvider(),
    )
    return service, sessions, accounts


class TestFinalizeBankConnection:
    @pytest.mark.asyncio
    async def test_raises_not_found_for_unknown_session(self) -> None:
        service, _, _ = _make_service()

        with pytest.raises(ConnectionSessionNotFound):
            await service(session_id=uuid4(), user_id=uuid4())

    @pytest.mark.asyncio
    async def test_raises_expired_for_expired_session(self) -> None:
        sessions = InMemoryConnectionSessionRepository()
        session = _make_session(expires_at=_NOW - timedelta(seconds=1))
        await sessions.add(session)
        service, _, _ = _make_service(sessions=sessions)

        with pytest.raises(ConnectionSessionExpired):
            await service(session_id=session.id, user_id=session.user_id)

    @pytest.mark.asyncio
    async def test_returns_accounts_and_persists_them(self) -> None:
        sessions = InMemoryConnectionSessionRepository()
        user_id = uuid4()
        session = _make_session(user_id=user_id)
        await sessions.add(session)

        provider = FakeOpenBankingProvider(
            accounts=[
                BankAccountInfo(
                    external_id="acc-1",
                    iban="LT12 3456 7890 1234 5678",
                    currency="EUR",
                    name="Main account",
                ),
            ]
        )
        service, _, accounts_repo = _make_service(provider=provider, sessions=sessions)

        result = await service(session_id=session.id, user_id=user_id)

        assert len(result) == 1
        assert result[0].external_id == "acc-1"
        assert result[0].user_id == user_id
        stored = await accounts_repo.get_by_external_id("acc-1")
        assert stored is not None

    @pytest.mark.asyncio
    async def test_does_not_duplicate_existing_accounts(self) -> None:
        sessions = InMemoryConnectionSessionRepository()
        accounts_repo = InMemoryAccountRepository()
        user_id = uuid4()
        session = _make_session(user_id=user_id)
        await sessions.add(session)

        provider = FakeOpenBankingProvider(
            accounts=[
                BankAccountInfo(
                    external_id="acc-1",
                    iban="LT12 3456 7890 1234 5678",
                    currency="EUR",
                    name="Main account",
                ),
            ]
        )
        service, _, _ = _make_service(
            provider=provider,
            sessions=sessions,
            accounts=accounts_repo,
        )

        await service(session_id=session.id, user_id=user_id)

        sessions2 = InMemoryConnectionSessionRepository()
        session2 = _make_session(user_id=user_id)
        await sessions2.add(session2)
        uow2 = FakeUnitOfWork(
            users=InMemoryUserRepository(),
            refresh_tokens=InMemoryRefreshTokenRepository(),
            accounts=accounts_repo,
            connection_sessions=sessions2,
        )
        service2 = FinalizeBankConnection(
            uow_factory=lambda: uow2,
            clock=FixedClock(_NOW),
            provider=provider,
        )
        result = await service2(session_id=session2.id, user_id=user_id)

        assert len(result) == 1
        all_accounts = await accounts_repo.list_by_user(user_id)
        assert len(all_accounts) == 1

    @pytest.mark.asyncio
    async def test_marks_session_as_linked(self) -> None:
        sessions = InMemoryConnectionSessionRepository()
        session = _make_session()
        await sessions.add(session)

        service, _, _ = _make_service(sessions=sessions)
        await service(session_id=session.id, user_id=session.user_id)

        assert session.status == ConnectionStatus.LINKED
