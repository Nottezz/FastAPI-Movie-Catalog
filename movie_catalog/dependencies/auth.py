import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request

from movie_catalog.services.auth import redis_users

logger = logging.getLogger(__name__)


UNSAFE_METHOD = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)
user_basic_auth = HTTPBasic(
    scheme_name="Basic auth",
    description="Basic username + password auth",
    auto_error=False,
)


def validate_basic_auth(credentials: HTTPBasicCredentials | None) -> None:
    logger.debug("User credentials: %s", credentials)

    if credentials and redis_users.validate_user_password(
        username=credentials.username, password=credentials.password
    ):
        return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password.",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(user_basic_auth)
    ] = None,
) -> None:
    if request.method not in UNSAFE_METHOD:
        return

    validate_basic_auth(credentials=credentials)
