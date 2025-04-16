import logging
from typing import Annotated

from fastapi import HTTPException, status, BackgroundTasks, Request, Header

from config import API_TOKENS
from schemas.movie_catalog import Movie
from .crud import storage

logger = logging.getLogger(__name__)

UNSAFE_METHOD = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
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


def validate_api_token(api_token: Annotated[str, Header(alias="x-auth-token")]):
    if api_token not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )
