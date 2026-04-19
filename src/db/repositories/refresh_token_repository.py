from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.refresh_token import RefreshTokenModel
from src.domain.entities.refresh_token import RefreshToken


class PostgresRefreshTokenRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add(self, token: RefreshToken) -> None:
        self._session.add(self._to_model(token))

    async def update(self, token: RefreshToken) -> None:
        await self._session.merge(self._to_model(token))

    async def get_by_hash(self, token_hash: bytes) -> RefreshToken | None:
        stmt = select(RefreshTokenModel).where(
            RefreshTokenModel.token_hash == token_hash,
        )
        model = (await self._session.execute(stmt)).scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def revoke_all_for_user(self, user_id: UUID, now: datetime) -> None:
        stmt = (
            update(RefreshTokenModel)
            .where(
                RefreshTokenModel.user_id == user_id,
                RefreshTokenModel.revoked_at.is_(None),
            )
            .values(revoked_at=now)
        )
        await self._session.execute(stmt)

    @staticmethod
    def _to_entity(model: RefreshTokenModel) -> RefreshToken:
        return RefreshToken(
            id=model.id,
            user_id=model.user_id,
            token_hash=model.token_hash,
            created_at=model.created_at,
            expires_at=model.expires_at,
            revoked_at=model.revoked_at,
        )

    @staticmethod
    def _to_model(entity: RefreshToken) -> RefreshTokenModel:
        return RefreshTokenModel(
            id=entity.id,
            user_id=entity.user_id,
            token_hash=entity.token_hash,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
            revoked_at=entity.revoked_at,
        )
