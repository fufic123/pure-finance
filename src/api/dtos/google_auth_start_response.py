from pydantic import BaseModel


class GoogleAuthStartResponse(BaseModel):
    authorization_url: str
