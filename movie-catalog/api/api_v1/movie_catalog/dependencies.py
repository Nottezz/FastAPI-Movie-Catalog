import logging

from fastapi import HTTPException, status, BackgroundTasks

from schemas.movie_catalog import Movie
from .crud import storage

logger = logging.getLogger(__name__)


def prefetch_film(movie_slug: str) -> Movie:
    films: Movie | None = storage.get_by_slug(movie_slug)
    if films:
        return films
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie {movie_slug!r} not found"
    )


def save_storage_state(background_tasks: BackgroundTasks):
    yield
    logger.debug("Add background tasks to save storage")
    background_tasks.add_task(storage.save_storage)
