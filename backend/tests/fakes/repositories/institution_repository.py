from uuid import UUID

from src.domain.entities.institution import Institution


class InMemoryInstitutionRepository:
    def __init__(self, institutions: list[Institution] | None = None) -> None:
        self._by_id: dict[UUID, Institution] = {}
        for inst in institutions or []:
            self._by_id[inst.id] = inst

    async def list_all(self) -> list[Institution]:
        return sorted(self._by_id.values(), key=lambda i: i.name)

    async def get_by_id(self, institution_id: UUID) -> Institution | None:
        return self._by_id.get(institution_id)

    async def add(self, institution: Institution) -> None:
        self._by_id[institution.id] = institution
