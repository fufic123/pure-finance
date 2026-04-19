from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.app.exceptions.cannot_delete_system_category import CannotDeleteSystemCategory
from src.app.exceptions.category_not_found import CategoryNotFound
from src.app.services.categories.delete_category import DeleteCategory
from src.domain.entities.category import Category
from tests.fakes.repositories.category_repository import InMemoryCategoryRepository
from tests.fakes.repositories.refresh_token_repository import InMemoryRefreshTokenRepository
from tests.fakes.repositories.user_repository import InMemoryUserRepository
from tests.fakes.unit_of_work import FakeUnitOfWork

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)
_USER_ID = uuid4()


def _system_category() -> Category:
    return Category(
        id=uuid4(),
        user_id=None,
        parent_id=None,
        name="Food & Drink",
        is_system=True,
        created_at=_NOW,
    )


def _user_category(user_id=_USER_ID) -> Category:
    return Category(
        id=uuid4(),
        user_id=user_id,
        parent_id=None,
        name="My Category",
        is_system=False,
        created_at=_NOW,
    )


def _make_service(categories: list[Category]) -> DeleteCategory:
    uow = FakeUnitOfWork(
        users=InMemoryUserRepository(),
        refresh_tokens=InMemoryRefreshTokenRepository(),
        categories=InMemoryCategoryRepository(categories),
    )
    return DeleteCategory(uow_factory=lambda: uow)


class TestDeleteCategory:
    @pytest.mark.asyncio
    async def test_deletes_user_category(self) -> None:
        cat = _user_category()
        service = _make_service([cat])

        await service(category_id=cat.id, user_id=_USER_ID)

    @pytest.mark.asyncio
    async def test_raises_when_system_category(self) -> None:
        cat = _system_category()
        service = _make_service([cat])

        with pytest.raises(CannotDeleteSystemCategory):
            await service(category_id=cat.id, user_id=_USER_ID)

    @pytest.mark.asyncio
    async def test_raises_when_not_owned_by_user(self) -> None:
        other_user = uuid4()
        cat = _user_category(user_id=other_user)
        service = _make_service([cat])

        with pytest.raises(CategoryNotFound):
            await service(category_id=cat.id, user_id=_USER_ID)

    @pytest.mark.asyncio
    async def test_raises_when_category_not_found(self) -> None:
        service = _make_service([])

        with pytest.raises(CategoryNotFound):
            await service(category_id=uuid4(), user_id=_USER_ID)
