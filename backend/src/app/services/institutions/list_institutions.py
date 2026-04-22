from typing import Callable

from src.app.ports.unit_of_work import UnitOfWork
from src.domain.entities.institution import Institution


class ListInstitutions:
    def __init__(self, uow_factory: Callable[[], UnitOfWork]) -> None:
        self._uow_factory = uow_factory

    async def __call__(self) -> list[Institution]:
        async with self._uow_factory() as uow:
            return await uow.institutions.list_all()
