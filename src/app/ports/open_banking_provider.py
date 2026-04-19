from typing import Protocol

from src.app.dtos.balance_info import BalanceInfo
from src.app.dtos.bank_account_info import BankAccountInfo
from src.app.dtos.institution_info import InstitutionInfo
from src.app.dtos.requisition_info import RequisitionInfo
from src.app.dtos.transaction_info import TransactionInfo


class OpenBankingProvider(Protocol):
    async def list_institutions(self, country: str) -> list[InstitutionInfo]: ...

    async def create_requisition(
        self,
        institution_id: str,
        redirect_uri: str,
        reference: str,
    ) -> RequisitionInfo: ...

    async def list_accounts(self, requisition_id: str) -> list[BankAccountInfo]: ...

    async def list_transactions(self, account_external_id: str) -> list[TransactionInfo]: ...

    async def get_balance(self, account_external_id: str) -> BalanceInfo | None: ...
