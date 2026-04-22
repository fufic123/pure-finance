from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.app.services.analytics.get_by_category import CategoryTotal


class AnalyticsByCategoryResponse(BaseModel):
    category_id: UUID | None
    total: Decimal
    count: int

    @classmethod
    def from_category_total(cls, ct: CategoryTotal) -> "AnalyticsByCategoryResponse":
        return cls(
            category_id=ct.category_id,
            total=ct.total,
            count=ct.count,
        )
