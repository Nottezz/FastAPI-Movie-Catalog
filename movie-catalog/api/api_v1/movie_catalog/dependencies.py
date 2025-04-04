from fastapi import HTTPException, status

from schemas.movie_catalog import Movie
from .crud import storage


def prefetch_film(movie_slug: str) -> Movie:
    films: Movie | None = storage.get_by_slug(movie_slug)
    if films:
        return films
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie {movie_slug!r} not found"
    )
