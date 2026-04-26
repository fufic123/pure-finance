from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.dependencies import (
    get_create_category,
    get_current_user,
    get_delete_category,
    get_list_categories,
)
from src.api.dtos.categories.create_request import CreateCategoryRequest
from src.api.dtos.categories.response import CategoryResponse
from src.app.services.categories.create_category import CreateCategory
from src.app.services.categories.delete_category import DeleteCategory
from src.app.services.categories.list_categories import ListCategories
from src.domain.entities.user import User

router = APIRouter()


@router.get("/categories", response_model=list[CategoryResponse])
async def list_categories(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListCategories, Depends(get_list_categories)],
) -> list[CategoryResponse]:
    categories = await service(user.id)
    return [CategoryResponse.from_category(c) for c in categories]


@router.post("/categories", response_model=CategoryResponse, status_code=201)
async def create_category(
    body: CreateCategoryRequest,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[CreateCategory, Depends(get_create_category)],
) -> CategoryResponse:
    category = await service(user_id=user.id, name=body.name, parent_id=body.parent_id)
    return CategoryResponse.from_category(category)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[DeleteCategory, Depends(get_delete_category)],
) -> None:
    await service(category_id=category_id, user_id=user.id)
