from datetime import UTC, datetime
from uuid import uuid4

from src.domain.entities.categorization_rule import CategorizationRule

_NOW = datetime(2026, 4, 19, 12, 0, 0, tzinfo=UTC)


def _rule(keyword: str) -> CategorizationRule:
    return CategorizationRule(
        id=uuid4(),
        user_id=uuid4(),
        category_id=uuid4(),
        keyword=keyword,
        created_at=_NOW,
    )


class TestCategorizationRuleMatches:
    def test_matches_exact(self) -> None:
        assert _rule("starbucks").matches("starbucks") is True

    def test_matches_case_insensitive(self) -> None:
        assert _rule("Starbucks").matches("STARBUCKS coffee") is True

    def test_matches_substring(self) -> None:
        assert _rule("bucks").matches("Payment to Starbucks") is True

    def test_no_match_when_keyword_absent(self) -> None:
        assert _rule("mcdonalds").matches("Payment to Starbucks") is False

    def test_empty_description_no_match(self) -> None:
        assert _rule("coffee").matches("") is False
