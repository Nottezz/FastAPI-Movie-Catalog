import logging
from typing import Annotated

from dependencies.auth import user_basic_auth, validate_basic_auth
from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)
from services.auth import redis_tokens
from storage.movie_catalog.crud import storage

from movie_catalog.schemas.movie_catalog import Movie

logger = logging.getLogger(__name__)

static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)


def prefetch_film(slug: str) -> Movie:
    films: Movie | None = storage.get_by_slug(slug)
    if films:
        return films
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie {slug!r} not found"
    )


def validate_api_token(api_token: HTTPAuthorizationCredentials) -> None:
    logger.debug("API token: %s", api_token)
    if redis_tokens.token_exists(api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_required(
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_api_token)
    ] = None,
) -> None:

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    validate_api_token(api_token=api_token)


def api_token_or_user_basic_auth_required(
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_api_token)
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(user_basic_auth)
    ] = None,
) -> None:
    if credentials:
        return validate_basic_auth(credentials=credentials)  # type: ignore[no-any-return]
    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth required",
    )
