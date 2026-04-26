from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.institution import Institution


class InstitutionResponse(BaseModel):
    id: UUID
    name: str

    @classmethod
    def from_institution(cls, institution: Institution) -> "InstitutionResponse":
        return cls(id=institution.id, name=institution.name)
