from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.institution import InstitutionModel
from src.domain.entities.institution import Institution


class PostgresInstitutionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_all(self) -> list[Institution]:
        stmt = select(InstitutionModel).order_by(InstitutionModel.name)
        models = (await self._session.execute(stmt)).scalars().all()
        return [self._to_entity(m) for m in models]

    async def get_by_id(self, institution_id: UUID) -> Institution | None:
        model = await self._session.get(InstitutionModel, institution_id)
        return self._to_entity(model) if model else None

    async def add(self, institution: Institution) -> None:
        self._session.add(self._to_model(institution))

    @staticmethod
    def _to_entity(model: InstitutionModel) -> Institution:
        return Institution(id=model.id, name=model.name, created_at=model.created_at)

    @staticmethod
    def _to_model(entity: Institution) -> InstitutionModel:
        return InstitutionModel(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
        )
