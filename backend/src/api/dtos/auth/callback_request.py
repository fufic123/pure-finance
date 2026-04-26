from pydantic import BaseModel


class GoogleCallbackRequest(BaseModel):
    code: str
    redirect_uri: str
    state: str
