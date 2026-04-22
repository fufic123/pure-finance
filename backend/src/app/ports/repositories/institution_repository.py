from typing import Protocol
from uuid import UUID

from src.domain.entities.institution import Institution


class InstitutionRepository(Protocol):
    async def list_all(self) -> list[Institution]: ...

    async def get_by_id(self, institution_id: UUID) -> Institution | None: ...

    async def add(self, institution: Institution) -> None: ...
