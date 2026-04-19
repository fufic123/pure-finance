from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BankAccountInfo:
    external_id: str
    iban: str | None
    currency: str
    name: str
