from fastapi import HTTPException, status

from schemas.movie_catalog import Movie
from .crud import MOVIE_LIST


def prefetch_film(movie_slug: str) -> Movie:
    films: Movie | None = next(
        (film for film in MOVIE_LIST if film.slug == movie_slug),
        None,
    )
    if films:
        return films

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Films not found")
