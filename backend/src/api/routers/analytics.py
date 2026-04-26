from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import (
    get_analytics_by_category,
    get_analytics_summary,
    get_current_user,
)
from src.api.dtos.analytics.by_category_response import AnalyticsByCategoryResponse
from src.api.dtos.analytics.summary_response import AnalyticsSummaryResponse
from src.app.services.analytics.get_by_category import GetAnalyticsByCategory
from src.app.services.analytics.get_summary import GetAnalyticsSummary
from src.domain.entities.user import User

router = APIRouter(prefix="/analytics")


@router.get("/summary", response_model=AnalyticsSummaryResponse)
async def get_summary(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[GetAnalyticsSummary, Depends(get_analytics_summary)],
    account_id: Annotated[UUID | None, Query()] = None,
    from_date: Annotated[date | None, Query(alias="from")] = None,
    to_date: Annotated[date | None, Query(alias="to")] = None,
) -> AnalyticsSummaryResponse:
    summary = await service(
        user_id=user.id,
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
    )
    return AnalyticsSummaryResponse.from_summary(summary)


@router.get("/by-category", response_model=list[AnalyticsByCategoryResponse])
async def get_by_category(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[GetAnalyticsByCategory, Depends(get_analytics_by_category)],
    account_id: Annotated[UUID | None, Query()] = None,
    from_date: Annotated[date | None, Query(alias="from")] = None,
    to_date: Annotated[date | None, Query(alias="to")] = None,
) -> list[AnalyticsByCategoryResponse]:
    totals = await service(
        user_id=user.id,
        account_id=account_id,
        from_date=from_date,
        to_date=to_date,
    )
    return [AnalyticsByCategoryResponse.from_category_total(ct) for ct in totals]
