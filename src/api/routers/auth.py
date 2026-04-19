from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import Response

from src.api.dependencies import (
    get_current_user,
    get_google_callback,
    get_logout,
    get_refresh_tokens,
    get_start_google_auth,
    rate_limit_auth,
)
from src.api.dtos.google_auth_start_request import GoogleAuthStartRequest
from src.api.dtos.google_auth_start_response import GoogleAuthStartResponse
from src.api.dtos.google_callback_request import GoogleCallbackRequest
from src.api.dtos.logout_request import LogoutRequest
from src.api.dtos.refresh_request import RefreshRequest
from src.api.dtos.token_pair_response import TokenPairResponse
from src.api.dtos.user_response import UserResponse
from src.app.services.auth.google_callback import GoogleCallback
from src.app.services.auth.logout import Logout
from src.app.services.auth.refresh_tokens import RefreshTokens
from src.app.services.auth.start_google_auth import StartGoogleAuth
from src.domain.entities.user import User

router = APIRouter(prefix="/auth")


@router.post(
    "/google",
    response_model=GoogleAuthStartResponse,
    dependencies=[Depends(rate_limit_auth)],
)
async def start_google_auth(
    body: GoogleAuthStartRequest,
    service: Annotated[StartGoogleAuth, Depends(get_start_google_auth)],
) -> GoogleAuthStartResponse:
    url = await service(body.redirect_uri)
    return GoogleAuthStartResponse(authorization_url=url)


@router.post(
    "/google/callback",
    response_model=TokenPairResponse,
    dependencies=[Depends(rate_limit_auth)],
)
async def google_callback(
    body: GoogleCallbackRequest,
    service: Annotated[GoogleCallback, Depends(get_google_callback)],
) -> TokenPairResponse:
    pair = await service(
        code=body.code,
        redirect_uri=body.redirect_uri,
        state=body.state,
    )
    return TokenPairResponse(access=pair.access, refresh=pair.refresh)


@router.post(
    "/refresh",
    response_model=TokenPairResponse,
    dependencies=[Depends(rate_limit_auth)],
)
async def refresh(
    body: RefreshRequest,
    service: Annotated[RefreshTokens, Depends(get_refresh_tokens)],
) -> TokenPairResponse:
    pair = await service(body.refresh)
    return TokenPairResponse(access=pair.access, refresh=pair.refresh)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(rate_limit_auth)],
)
async def logout(
    body: LogoutRequest,
    service: Annotated[Logout, Depends(get_logout)],
) -> Response:
    await service(body.refresh)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/me", response_model=UserResponse)
async def me(user: Annotated[User, Depends(get_current_user)]) -> UserResponse:
    return UserResponse.from_user(user)
