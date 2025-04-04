from fastapi import APIRouter, status

from schemas.movie_catalog import Movie, MovieCreate
from api.api_v1.movie_catalog.crud import storage

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[Movie],
)
def get_movie_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=Movie,
    status_code=status.HTTP_201_CREATED,
)
def add_movie(
    movie_create: MovieCreate,
) -> Movie:
    return storage.create(movie_create)
