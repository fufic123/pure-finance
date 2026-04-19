from uuid import UUID

from pydantic import BaseModel, Field


class CreateRuleRequest(BaseModel):
    category_id: UUID
    keyword: str = Field(min_length=1, max_length=200)
