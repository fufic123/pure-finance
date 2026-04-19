from uuid import UUID

from pydantic import BaseModel


class UpdateTransactionRequest(BaseModel):
    note: str | None = None
    category_id: UUID | None = None
