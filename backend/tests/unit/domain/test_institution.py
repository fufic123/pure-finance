from datetime import UTC, datetime

import pytest

from src.domain.entities.institution import Institution
from src.domain.exceptions.institution_name_invalid import InstitutionNameInvalid


class _FrozenClock:
    def now(self) -> datetime:
        return datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


class TestInstitutionCreate:
    def test_accepts_normal_name(self) -> None:
        inst = Institution.create(name="SEB", clock=_FrozenClock())
        assert inst.name == "SEB"
        assert inst.id is not None
        assert inst.created_at == datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)

    def test_rejects_empty_name(self) -> None:
        with pytest.raises(InstitutionNameInvalid):
            Institution.create(name="", clock=_FrozenClock())

    def test_rejects_too_long_name(self) -> None:
        with pytest.raises(InstitutionNameInvalid):
            Institution.create(name="x" * 81, clock=_FrozenClock())

    def test_accepts_max_length_name(self) -> None:
        inst = Institution.create(name="x" * 80, clock=_FrozenClock())
        assert len(inst.name) == 80
