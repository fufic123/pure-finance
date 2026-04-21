from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class InstitutionInfo:
    external_id: str
    name: str
    country: str
    logo_url: str | None = None
