from fastapi import APIRouter, status, BackgroundTasks

from schemas.movie_catalog import Movie, MovieCreate, MovieRead
from api.api_v1.movie_catalog.crud import storage

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


@router.get(
    "/",
    response_model=list[MovieRead],
)
def get_movie_list() -> list[Movie]:
    return storage.get()


@router.post(
    "/",
    response_model=MovieRead,
    status_code=status.HTTP_201_CREATED,
)
def add_movie(
    movie_create: MovieCreate,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_storage)
    return storage.create(movie_create)
