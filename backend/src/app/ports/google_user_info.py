from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GoogleUserInfo:
    google_id: str
    email: str
