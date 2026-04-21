from decimal import Decimal

from pydantic import BaseModel

from src.app.services.analytics.get_summary import AnalyticsSummary


class AnalyticsSummaryResponse(BaseModel):
    income_eur: Decimal
    expenses_eur: Decimal
    net_eur: Decimal
    transaction_count: int
    transactions_without_fx: int

    @classmethod
    def from_summary(cls, summary: AnalyticsSummary) -> "AnalyticsSummaryResponse":
        return cls(
            income_eur=summary.income_eur,
            expenses_eur=summary.expenses_eur,
            net_eur=summary.net_eur,
            transaction_count=summary.transaction_count,
            transactions_without_fx=summary.transactions_without_fx,
        )
