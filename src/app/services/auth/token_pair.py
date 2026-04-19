from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TokenPair:
    access: str
    refresh: str
