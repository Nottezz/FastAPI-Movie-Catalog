import random
from typing import Annotated

from annotated_types import Len
from fastapi import APIRouter, Depends, status, Form

from schemas.movie_catalog import MovieCatalog
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
    title: Annotated[str, Len(min_length=3, max_length=50), Form()],
    description: Annotated[str, Len(min_length=20, max_length=500), Form()],
    year_released: Annotated[int, Form()],
    rating: Annotated[float, Form()],
) -> MovieCatalog:
    return MovieCatalog(
        id=random.randint(1, 100),
        title=title,
        description=description,
        year_released=year_released,
        rating=rating,
    )


@router.get("/{movie_id}", response_model=MovieCatalog)
def get_movie(
    movie_id: Annotated[MovieCatalog, Depends(prefetch_film)]
) -> MovieCatalog:
    return movie_id
