from pydantic import BaseModel


class StartConnectionRequest(BaseModel):
    institution_id: str
    redirect_uri: str
