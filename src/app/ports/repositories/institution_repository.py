from typing import Protocol
from uuid import UUID

from src.domain.entities.institution import Institution


class InstitutionRepository(Protocol):
    async def add(self, institution: Institution) -> None: ...

    async def get_by_external_id(self, external_id: str) -> Institution | None: ...

    async def list_by_country(self, country: str) -> list[Institution]: ...
