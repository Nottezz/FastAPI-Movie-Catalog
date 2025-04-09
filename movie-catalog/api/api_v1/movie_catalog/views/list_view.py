from fastapi import APIRouter, status, Depends

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import save_storage_state
from schemas.movie_catalog import Movie, MovieCreate, MovieRead

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
    dependencies=[Depends(save_storage_state)],
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
    _=Depends(save_storage_state),
) -> Movie:
    return storage.create(movie_create)
