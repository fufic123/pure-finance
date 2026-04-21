from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(slots=True)
class Institution:
    id: UUID
    external_id: str
    name: str
    country: str
    logo_url: str | None = None

    @classmethod
    def from_provider(
        cls,
        external_id: str,
        name: str,
        country: str,
        logo_url: str | None = None,
    ) -> "Institution":
        return cls(
            id=uuid4(),
            external_id=external_id,
            name=name,
            country=country,
            logo_url=logo_url,
        )
