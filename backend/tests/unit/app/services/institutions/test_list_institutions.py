from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.app.services.institutions.list_institutions import ListInstitutions
from src.domain.entities.institution import Institution
from tests.fakes.repositories.institution_repository import InMemoryInstitutionRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork


def _make_inst(name: str) -> Institution:
    return Institution(id=uuid4(), name=name, created_at=datetime(2026, 4, 21, tzinfo=UTC))


@pytest.mark.asyncio
async def test_returns_all_institutions_sorted() -> None:
    institutions = [_make_inst("Swedbank"), _make_inst("SEB"), _make_inst("LHV")]
    repo = InMemoryInstitutionRepository(institutions)
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        institutions=repo,
    )

    service = ListInstitutions(uow_factory=lambda: uow)
    result = await service()

    assert [i.name for i in result] == ["LHV", "SEB", "Swedbank"]


@pytest.mark.asyncio
async def test_returns_empty_when_no_institutions() -> None:
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
    )

    service = ListInstitutions(uow_factory=lambda: uow)
    result = await service()

    assert result == []
