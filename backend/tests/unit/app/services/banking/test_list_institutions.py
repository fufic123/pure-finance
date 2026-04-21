import pytest

from src.app.dtos.institution_info import InstitutionInfo
from src.app.services.banking.list_institutions import ListInstitutions
from tests.fakes.open_banking_provider import FakeOpenBankingProvider


class TestListInstitutions:
    @pytest.mark.asyncio
    async def test_returns_institutions_from_provider(self) -> None:
        provider = FakeOpenBankingProvider(
            institutions=[
                InstitutionInfo(
                    external_id="REVOLUT_LT",
                    name="Revolut",
                    country="LT",
                    logo_url="https://cdn.example.com/revolut.png",
                ),
                InstitutionInfo(
                    external_id="SWEDBANK_LT",
                    name="Swedbank",
                    country="LT",
                    logo_url=None,
                ),
            ]
        )
        service = ListInstitutions(provider=provider)

        result = await service("LT")

        assert len(result) == 2
        assert result[0].external_id == "REVOLUT_LT"
        assert result[0].name == "Revolut"
        assert result[0].country == "LT"
        assert result[0].logo_url == "https://cdn.example.com/revolut.png"
        assert result[1].external_id == "SWEDBANK_LT"
        assert result[1].logo_url is None

    @pytest.mark.asyncio
    async def test_returns_empty_list_when_no_institutions(self) -> None:
        provider = FakeOpenBankingProvider(institutions=[])
        service = ListInstitutions(provider=provider)

        result = await service("XX")

        assert result == []
