from fastapi import FastAPI

from src.api.response_handlers.app_errors import (
    handle_access_token_invalid,
    handle_account_not_found,
    handle_cannot_delete_system_category,
    handle_category_not_found,
    handle_institution_not_found,
    handle_oauth_state_invalid,
    handle_rate_limit_exceeded,
    handle_rule_not_found,
    handle_transaction_not_found,
)
from src.api.response_handlers.domain_errors import (
    handle_refresh_token_expired,
    handle_refresh_token_not_found,
    handle_refresh_token_revoked,
    handle_user_not_found,
)
from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.cannot_delete_system_category import CannotDeleteSystemCategory
from src.app.exceptions.category_not_found import CategoryNotFound
from src.app.exceptions.institution_not_found import InstitutionNotFound
from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid
from src.app.exceptions.rate_limit_exceeded import RateLimitExceeded
from src.app.exceptions.rule_not_found import RuleNotFound
from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.domain.exceptions.refresh_token_expired import RefreshTokenExpired
from src.domain.exceptions.refresh_token_not_found import RefreshTokenNotFound
from src.domain.exceptions.refresh_token_revoked import RefreshTokenRevoked
from src.domain.exceptions.user_not_found import UserNotFound


def install_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AccessTokenInvalid, handle_access_token_invalid)
    app.add_exception_handler(AccountNotFound, handle_account_not_found)
    app.add_exception_handler(CategoryNotFound, handle_category_not_found)
    app.add_exception_handler(InstitutionNotFound, handle_institution_not_found)
    app.add_exception_handler(CannotDeleteSystemCategory, handle_cannot_delete_system_category)
    app.add_exception_handler(RuleNotFound, handle_rule_not_found)
    app.add_exception_handler(TransactionNotFound, handle_transaction_not_found)
    app.add_exception_handler(OAuthStateInvalid, handle_oauth_state_invalid)
    app.add_exception_handler(RateLimitExceeded, handle_rate_limit_exceeded)
    app.add_exception_handler(RefreshTokenNotFound, handle_refresh_token_not_found)
    app.add_exception_handler(RefreshTokenRevoked, handle_refresh_token_revoked)
    app.add_exception_handler(RefreshTokenExpired, handle_refresh_token_expired)
    app.add_exception_handler(UserNotFound, handle_user_not_found)
