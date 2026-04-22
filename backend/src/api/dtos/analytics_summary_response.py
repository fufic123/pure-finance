from decimal import Decimal

from pydantic import BaseModel

from src.app.services.analytics.get_summary import AnalyticsSummary


class AnalyticsSummaryResponse(BaseModel):
    income: Decimal
    expenses: Decimal
    net: Decimal
    transaction_count: int

    @classmethod
    def from_summary(cls, summary: AnalyticsSummary) -> "AnalyticsSummaryResponse":
        return cls(
            income=summary.income,
            expenses=summary.expenses,
            net=summary.net,
            transaction_count=summary.transaction_count,
        )
