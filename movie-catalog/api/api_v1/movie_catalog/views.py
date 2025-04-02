from typing import Annotated

from fastapi import APIRouter, Depends

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
def get_films_list() -> list[MovieCatalog]:
    return MOVIE_LIST


@router.get("/{movie_id}", response_model=MovieCatalog)
def get_film(movie_id: Annotated[MovieCatalog, Depends(prefetch_film)]) -> MovieCatalog:
    return movie_id
