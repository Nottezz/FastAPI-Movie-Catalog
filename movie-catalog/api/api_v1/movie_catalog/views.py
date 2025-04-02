import random
from typing import Annotated

from fastapi import APIRouter, Depends, status

from schemas.movie_catalog import MovieCatalog, MovieCatalogCreate
from .crud import MOVIE_LIST
from .dependencies import prefetch_film

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[MovieCatalog],
)
def get_movie_list() -> list[MovieCatalog]:
    return MOVIE_LIST


@router.post(
    "/",
    response_model=MovieCatalog,
    status_code=status.HTTP_201_CREATED,
)
def add_movie(
    movie_create: MovieCatalogCreate,
) -> MovieCatalog:
    return MovieCatalog(
        **movie_create.model_dump(),
    )


@router.get("/{slug}", response_model=MovieCatalog)
def get_movie(
    movie_slug: Annotated[MovieCatalog, Depends(prefetch_film)]
) -> MovieCatalog:
    return movie_slug
