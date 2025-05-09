import logging
from typing import Annotated

from fastapi import HTTPException, status, BackgroundTasks, Request, Depends
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)

import config
from config import USERS_DB
from schemas.movie_catalog import Movie
from .crud import storage
from .redis import redis_tokens

logger = logging.getLogger(__name__)

UNSAFE_METHOD = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)
static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your **Static API token** from the developer portal. [Read more](#)",
    auto_error=False,
)

user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username + password auth",
    auto_error=False,
)


def prefetch_film(movie_slug: str) -> Movie:
    films: Movie | None = storage.get_by_slug(movie_slug)
    if films:
        return films
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie {movie_slug!r} not found"
    )


def save_storage_state(background_tasks: BackgroundTasks, request: Request):
    yield
    if request.method in UNSAFE_METHOD:
        logger.debug("Add background tasks to save storage")
        background_tasks.add_task(storage.save_storage)


def validate_api_token(api_token: HTTPAuthorizationCredentials):

    logger.debug("API token: %s", api_token)
    if redis_tokens.sismember(config.REDIS_TOKENS_SET_NAME, api_token.credentials):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token",
    )


def api_token_required(
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_api_token)
    ] = None,
):

    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required",
        )

    validate_api_token(api_token=api_token)


def validate_basic_auth(credentials: HTTPBasicCredentials | None):
    logger.debug("User credentials: %s", credentials)

    if (
        credentials
        and credentials.username in USERS_DB
        and USERS_DB[credentials.username] == credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required(
    credentials: Annotated[HTTPBasicCredentials | None, Depends(user_basic_auth)] = None
):
    validate_basic_auth(credentials=credentials)


def api_token_or_user_basic_auth_required(
    api_token: Annotated[
        HTTPAuthorizationCredentials | None, Depends(static_api_token)
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(user_basic_auth)
    ] = None,
):
    if credentials:
        return validate_basic_auth(credentials=credentials)
    if api_token:
        return validate_api_token(api_token=api_token)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or basic auth required",
    )
