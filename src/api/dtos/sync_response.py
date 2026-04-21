from pydantic import BaseModel


class SyncResponse(BaseModel):
    added: int
