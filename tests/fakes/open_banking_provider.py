from src.app.dtos.balance_info import BalanceInfo
from src.app.dtos.bank_account_info import BankAccountInfo
from src.app.dtos.institution_info import InstitutionInfo
from src.app.dtos.requisition_info import RequisitionInfo
from src.app.dtos.transaction_info import TransactionInfo


class FakeOpenBankingProvider:
    def __init__(
        self,
        institutions: list[InstitutionInfo] | None = None,
        requisition: RequisitionInfo | None = None,
        accounts: list[BankAccountInfo] | None = None,
        transactions: list[TransactionInfo] | None = None,
        balance: BalanceInfo | None = None,
    ) -> None:
        self._institutions = institutions or []
        self._requisition = requisition or RequisitionInfo(
            requisition_id="req-123",
            link="https://ob.example.com/auth",
        )
        self._accounts = accounts or []
        self._transactions = transactions or []
        self._balance = balance

    async def list_institutions(self, country: str) -> list[InstitutionInfo]:
        return self._institutions

    async def create_requisition(
        self,
        institution_id: str,
        redirect_uri: str,
        reference: str,
    ) -> RequisitionInfo:
        return self._requisition

    async def list_accounts(self, requisition_id: str) -> list[BankAccountInfo]:
        return self._accounts

    async def list_transactions(self, account_external_id: str) -> list[TransactionInfo]:
        return self._transactions

    async def get_balance(self, account_external_id: str) -> BalanceInfo | None:
        return self._balance
