import random
from typing import Annotated

from fastapi import APIRouter, Depends, status

from schemas.movie_catalog import Movie, MovieCreate
from .crud import MOVIE_LIST
from .dependencies import prefetch_film

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def get_movie_list() -> list[Movie]:
    return MOVIE_LIST


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def add_movie(
    movie_create: MovieCreate,
) -> Movie:
    return Movie(
        **movie_create.model_dump(),
    )


@router.get("/{slug}", response_model=Movie)
def get_movie(movie_slug: Annotated[Movie, Depends(prefetch_film)]) -> Movie:
    return movie_slug
