from pydantic import BaseModel


class LogoutRequest(BaseModel):
    refresh: str
