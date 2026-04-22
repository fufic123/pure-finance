from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.dependencies import get_current_user, get_list_institutions
from src.api.dtos.institution_response import InstitutionResponse
from src.app.services.institutions.list_institutions import ListInstitutions
from src.domain.entities.user import User

router = APIRouter()


@router.get("/institutions", response_model=list[InstitutionResponse])
async def list_institutions(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[ListInstitutions, Depends(get_list_institutions)],
) -> list[InstitutionResponse]:
    institutions = await service()
    return [InstitutionResponse.from_institution(i) for i in institutions]
