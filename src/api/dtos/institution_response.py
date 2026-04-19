from pydantic import BaseModel

from src.domain.entities.institution import Institution


class InstitutionResponse(BaseModel):
    id: str
    name: str
    country: str
    logo_url: str | None

    @classmethod
    def from_institution(cls, institution: Institution) -> "InstitutionResponse":
        return cls(
            id=institution.external_id,
            name=institution.name,
            country=institution.country,
            logo_url=institution.logo_url,
        )
