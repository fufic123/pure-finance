from src.app.ports.open_banking_provider import OpenBankingProvider
from src.domain.entities.institution import Institution


class ListInstitutions:
    def __init__(self, provider: OpenBankingProvider) -> None:
        self._provider = provider

    async def __call__(self, country: str) -> list[Institution]:
        infos = await self._provider.list_institutions(country)
        return [
            Institution.from_provider(
                external_id=info.external_id,
                name=info.name,
                country=info.country,
                logo_url=info.logo_url,
            )
            for info in infos
        ]
