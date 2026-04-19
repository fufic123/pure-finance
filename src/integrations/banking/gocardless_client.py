from datetime import UTC, datetime
from decimal import Decimal

import httpx
from redis.asyncio import Redis

from src.app.dtos.balance_info import BalanceInfo
from src.app.dtos.bank_account_info import BankAccountInfo
from src.app.dtos.institution_info import InstitutionInfo
from src.app.dtos.requisition_info import RequisitionInfo
from src.app.dtos.transaction_info import TransactionInfo

_ACCESS_TOKEN_TTL = 82800   # 23 h (GoCardless issues 24 h tokens)
_CACHE_KEY = "gocardless:access_token"


class GoCardlessClient:
    _BASE_URL = "https://bankaccountdata.gocardless.com/api/v2"

    def __init__(
        self,
        secret_id: str,
        secret_key: str,
        http_client: httpx.AsyncClient,
        redis: Redis,
    ) -> None:
        self._secret_id = secret_id
        self._secret_key = secret_key
        self._http = http_client
        self._redis = redis

    async def list_institutions(self, country: str) -> list[InstitutionInfo]:
        token = await self._get_token()
        response = await self._http.get(
            f"{self._BASE_URL}/institutions/",
            params={"country": country},
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        return [
            InstitutionInfo(
                external_id=item["id"],
                name=item["name"],
                country=country,
                logo_url=item.get("logo"),
            )
            for item in response.json()
        ]

    async def create_requisition(
        self,
        institution_id: str,
        redirect_uri: str,
        reference: str,
    ) -> RequisitionInfo:
        token = await self._get_token()
        response = await self._http.post(
            f"{self._BASE_URL}/requisitions/",
            json={
                "institution_id": institution_id,
                "redirect": redirect_uri,
                "reference": reference,
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        data = response.json()
        return RequisitionInfo(
            requisition_id=data["id"],
            link=data["link"],
        )

    async def list_accounts(self, requisition_id: str) -> list[BankAccountInfo]:
        token = await self._get_token()
        req_response = await self._http.get(
            f"{self._BASE_URL}/requisitions/{requisition_id}/",
            headers={"Authorization": f"Bearer {token}"},
        )
        req_response.raise_for_status()
        account_ids: list[str] = req_response.json().get("accounts", [])

        accounts = []
        for account_id in account_ids:
            detail_response = await self._http.get(
                f"{self._BASE_URL}/accounts/{account_id}/details/",
                headers={"Authorization": f"Bearer {token}"},
            )
            detail_response.raise_for_status()
            detail = detail_response.json().get("account", {})
            accounts.append(
                BankAccountInfo(
                    external_id=account_id,
                    iban=detail.get("iban"),
                    currency=detail.get("currency", ""),
                    name=detail.get("name", detail.get("ownerName", "")),
                )
            )
        return accounts

    async def list_transactions(self, account_external_id: str) -> list[TransactionInfo]:
        token = await self._get_token()
        response = await self._http.get(
            f"{self._BASE_URL}/accounts/{account_external_id}/transactions/",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        booked = response.json().get("transactions", {}).get("booked", [])
        return [
            TransactionInfo(
                external_id=t["transactionId"],
                amount=Decimal(t["transactionAmount"]["amount"]),
                currency=t["transactionAmount"]["currency"],
                description=t.get("remittanceInformationUnstructured", ""),
                booked_at=datetime.fromisoformat(t["bookingDate"]).replace(tzinfo=UTC),
            )
            for t in booked
            if "transactionId" in t
        ]

    async def get_balance(self, account_external_id: str) -> BalanceInfo | None:
        token = await self._get_token()
        response = await self._http.get(
            f"{self._BASE_URL}/accounts/{account_external_id}/balances/",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        balances: list[dict] = response.json().get("balances", [])
        preferred = next(
            (b for b in balances if b.get("balanceType") == "interimAvailable"),
            balances[0] if balances else None,
        )
        if preferred is None:
            return None
        ba = preferred["balanceAmount"]
        return BalanceInfo(amount=Decimal(ba["amount"]), currency=ba["currency"])

    async def _get_token(self) -> str:
        cached = await self._redis.get(_CACHE_KEY)
        if cached:
            return cached

        response = await self._http.post(
            f"{self._BASE_URL}/token/new/",
            json={"secret_id": self._secret_id, "secret_key": self._secret_key},
        )
        response.raise_for_status()
        token: str = response.json()["access"]
        await self._redis.set(_CACHE_KEY, token, ex=_ACCESS_TOKEN_TTL)
        return token
