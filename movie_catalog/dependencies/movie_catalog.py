from typing import Annotated

from fastapi import Depends, HTTPException, Request
from schemas.movie_catalog import Movie
from starlette import status
from storage.movie_catalog import MovieCatalogStorage
from storage.movie_catalog.crud import storage


def get_movie_catalog_storage(
    request: Request,
) -> MovieCatalogStorage:
    return request.app.state.movie_catalog_storage


GetMovieCatalogStorage = Annotated[
    MovieCatalogStorage,
    Depends(get_movie_catalog_storage),
]


def prefetch_movie(slug: str) -> Movie:
    movie: Movie | None = storage.get_by_slug(slug)
    if movie:
        return movie
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie {slug!r} not found"
    )


MovieBySlug = Annotated[Movie, Depends(prefetch_movie)]
