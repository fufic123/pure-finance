from uuid import UUID

from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    parent_id: UUID | None = None
