from datetime import date
from decimal import Decimal

import pytest

from src.integrations.fx.ecb import _parse

_SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<gesmes:Envelope xmlns:gesmes="http://www.gesmes.org/xml/2002-08-01"
                 xmlns="http://www.ecb.int/vocabulary/2002-08-01/eurofxref">
    <gesmes:subject>Reference rates</gesmes:subject>
    <gesmes:Sender><gesmes:name>European Central Bank</gesmes:name></gesmes:Sender>
    <Cube>
        <Cube time="2026-04-18">
            <Cube currency="USD" rate="1.1000"/>
            <Cube currency="GBP" rate="0.8500"/>
            <Cube currency="PLN" rate="4.2500"/>
        </Cube>
    </Cube>
</gesmes:Envelope>"""


class TestEcbParser:
    def test_parses_date(self) -> None:
        rate_date, _ = _parse(_SAMPLE_XML)
        assert rate_date == date(2026, 4, 18)

    def test_parses_all_currencies(self) -> None:
        _, rates = _parse(_SAMPLE_XML)
        assert set(rates.keys()) == {"USD", "GBP", "PLN"}

    def test_parses_rate_values(self) -> None:
        _, rates = _parse(_SAMPLE_XML)
        assert rates["USD"] == Decimal("1.1000")
        assert rates["GBP"] == Decimal("0.8500")
        assert rates["PLN"] == Decimal("4.2500")

    def test_raises_on_missing_cube(self) -> None:
        with pytest.raises(ValueError, match="no Cube element"):
            _parse("<root/>")
