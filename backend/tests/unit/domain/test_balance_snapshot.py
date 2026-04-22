from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.domain.entities.balance_snapshot import BalanceSnapshot


class _FrozenClock:
    def now(self) -> datetime:
        return datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)


class TestBalanceSnapshotCreate:
    def test_creates_with_utc_datetime(self) -> None:
        account_id = uuid4()
        snap = BalanceSnapshot.create(
            account_id=account_id,
            amount=Decimal("100.00"),
            recorded_at=datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC),
            clock=_FrozenClock(),
        )
        assert snap.account_id == account_id
        assert snap.amount == Decimal("100.00")
        assert snap.recorded_at.tzinfo is not None
        assert snap.created_at == datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC)

    def test_rejects_naive_recorded_at(self) -> None:
        with pytest.raises(ValueError):
            BalanceSnapshot.create(
                account_id=uuid4(),
                amount=Decimal("100.00"),
                recorded_at=datetime(2026, 4, 21, 12, 0, 0),
                clock=_FrozenClock(),
            )

    def test_accepts_negative_amount_for_overdraft(self) -> None:
        snap = BalanceSnapshot.create(
            account_id=uuid4(),
            amount=Decimal("-50.25"),
            recorded_at=datetime(2026, 4, 21, 12, 0, 0, tzinfo=UTC),
            clock=_FrozenClock(),
        )
        assert snap.amount == Decimal("-50.25")
