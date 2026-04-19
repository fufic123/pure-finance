from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.user import UserModel
from src.domain.entities.user import User
from src.domain.exceptions.user_not_found import UserNotFound


class PostgresUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, user: User) -> None:
        self._session.add(self._to_model(user))

    async def get_by_id(self, user_id: UUID) -> User:
        model = await self._session.get(UserModel, user_id)
        if model is None:
            raise UserNotFound()
        return self._to_entity(model)

    async def get_by_google_id(self, google_id: str) -> User | None:
        stmt = select(UserModel).where(UserModel.google_id == google_id)
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    @staticmethod
    def _to_entity(model: UserModel) -> User:
        return User(
            id=model.id,
            google_id=model.google_id,
            email=model.email,
            created_at=model.created_at,
        )

    @staticmethod
    def _to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            google_id=entity.google_id,
            email=entity.email,
            created_at=entity.created_at,
        )
