import xml.etree.ElementTree as ET
from datetime import date
from decimal import Decimal

import httpx

_ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
_NS = {"ecb": "http://www.ecb.int/vocabulary/2002-08-01/eurofxref"}


class EcbFxRateProvider:
    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def get_rates(self) -> tuple[date, dict[str, Decimal]]:
        response = await self._client.get(_ECB_URL, timeout=10)
        response.raise_for_status()
        return _parse(response.text)


def _parse(xml_text: str) -> tuple[date, dict[str, Decimal]]:
    root = ET.fromstring(xml_text)
    cube_envelope = root.find(".//ecb:Cube[@time]", _NS)
    if cube_envelope is None:
        raise ValueError("ECB XML: no Cube element with time attribute")
    rate_date = date.fromisoformat(cube_envelope.attrib["time"])
    rates: dict[str, Decimal] = {}
    for cube in cube_envelope:
        currency = cube.attrib.get("currency")
        rate_str = cube.attrib.get("rate")
        if currency and rate_str:
            rates[currency] = Decimal(rate_str)
    return rate_date, rates
