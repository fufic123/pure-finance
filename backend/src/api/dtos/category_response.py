from uuid import UUID

from pydantic import BaseModel

from src.domain.entities.category import Category


class CategoryResponse(BaseModel):
    id: UUID
    parent_id: UUID | None
    name: str
    is_system: bool

    @classmethod
    def from_category(cls, category: Category) -> "CategoryResponse":
        return cls(
            id=category.id,
            parent_id=category.parent_id,
            name=category.name,
            is_system=category.is_system,
        )
