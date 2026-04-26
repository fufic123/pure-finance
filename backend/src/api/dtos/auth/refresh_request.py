from pydantic import BaseModel


class RefreshRequest(BaseModel):
    refresh: str
