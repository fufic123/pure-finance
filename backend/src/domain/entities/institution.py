from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from src.app.ports.clock import Clock
from src.domain.exceptions.institution_name_invalid import InstitutionNameInvalid

_NAME_MIN = 1
_NAME_MAX = 80


@dataclass(slots=True)
class Institution:
    id: UUID
    name: str
    created_at: datetime

    @classmethod
    def create(cls, name: str, clock: Clock) -> "Institution":
        if not _NAME_MIN <= len(name) <= _NAME_MAX:
            raise InstitutionNameInvalid()
        return cls(id=uuid4(), name=name, created_at=clock.now())
