from fastapi import APIRouter, status, Depends

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import (
    save_storage_state,
    user_basic_auth_required,
)
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
    dependencies=[
        Depends(user_basic_auth_required),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid API token",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token",
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "API token is required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "API token is required",
                    }
                }
            },
        },
    },
)
def add_movie(
    movie_create: MovieCreate,
    __=Depends(save_storage_state),
) -> Movie:
    return storage.create(movie_create)
