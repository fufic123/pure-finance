from fastapi import FastAPI

from src.api.response_handlers.app.access_token_invalid import (
    handle as handle_access_token_invalid,
)
from src.api.response_handlers.app.account_not_found import (
    handle as handle_account_not_found,
)
from src.api.response_handlers.app.cannot_delete_system_category import (
    handle as handle_cannot_delete_system_category,
)
from src.api.response_handlers.app.category_not_found import (
    handle as handle_category_not_found,
)
from src.api.response_handlers.app.rule_not_found import (
    handle as handle_rule_not_found,
)
from src.api.response_handlers.app.transaction_not_found import (
    handle as handle_transaction_not_found,
)
from src.api.response_handlers.app.connection_session_expired import (
    handle as handle_connection_session_expired,
)
from src.api.response_handlers.app.connection_session_not_found import (
    handle as handle_connection_session_not_found,
)
from src.api.response_handlers.app.oauth_state_invalid import (
    handle as handle_oauth_state_invalid,
)
from src.api.response_handlers.app.rate_limit_exceeded import (
    handle as handle_rate_limit_exceeded,
)
from src.api.response_handlers.domain.refresh_token_expired import (
    handle as handle_refresh_token_expired,
)
from src.api.response_handlers.domain.refresh_token_not_found import (
    handle as handle_refresh_token_not_found,
)
from src.api.response_handlers.domain.refresh_token_revoked import (
    handle as handle_refresh_token_revoked,
)
from src.api.response_handlers.domain.user_not_found import (
    handle as handle_user_not_found,
)
from src.app.exceptions.access_token_invalid import AccessTokenInvalid
from src.app.exceptions.account_not_found import AccountNotFound
from src.app.exceptions.cannot_delete_system_category import CannotDeleteSystemCategory
from src.app.exceptions.category_not_found import CategoryNotFound
from src.app.exceptions.rule_not_found import RuleNotFound
from src.app.exceptions.transaction_not_found import TransactionNotFound
from src.app.exceptions.connection_session_expired import ConnectionSessionExpired
from src.app.exceptions.connection_session_not_found import ConnectionSessionNotFound
from src.app.exceptions.oauth_state_invalid import OAuthStateInvalid
from src.app.exceptions.rate_limit_exceeded import RateLimitExceeded
from src.domain.exceptions.refresh_token_expired import RefreshTokenExpired
from src.domain.exceptions.refresh_token_not_found import RefreshTokenNotFound
from src.domain.exceptions.refresh_token_revoked import RefreshTokenRevoked
from src.domain.exceptions.user_not_found import UserNotFound


def install_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AccessTokenInvalid, handle_access_token_invalid)
    app.add_exception_handler(AccountNotFound, handle_account_not_found)
    app.add_exception_handler(CategoryNotFound, handle_category_not_found)
    app.add_exception_handler(CannotDeleteSystemCategory, handle_cannot_delete_system_category)
    app.add_exception_handler(RuleNotFound, handle_rule_not_found)
    app.add_exception_handler(TransactionNotFound, handle_transaction_not_found)
    app.add_exception_handler(ConnectionSessionNotFound, handle_connection_session_not_found)
    app.add_exception_handler(ConnectionSessionExpired, handle_connection_session_expired)
    app.add_exception_handler(OAuthStateInvalid, handle_oauth_state_invalid)
    app.add_exception_handler(RateLimitExceeded, handle_rate_limit_exceeded)
    app.add_exception_handler(RefreshTokenNotFound, handle_refresh_token_not_found)
    app.add_exception_handler(RefreshTokenRevoked, handle_refresh_token_revoked)
    app.add_exception_handler(RefreshTokenExpired, handle_refresh_token_expired)
    app.add_exception_handler(UserNotFound, handle_user_not_found)
