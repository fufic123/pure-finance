from pydantic import BaseModel


class GoogleAuthStartRequest(BaseModel):
    redirect_uri: str
