from pydantic import BaseModel


class TokenPairResponse(BaseModel):
    access: str
    refresh: str
