from fastapi import APIRouter, status, Depends

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import (
    api_token_or_user_basic_auth_required,
)
from schemas.movie_catalog import Movie, MovieCreate, MovieRead

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
    dependencies=[
        Depends(api_token_or_user_basic_auth_required),
    ],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Invalid API token or username and password",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid API token or username and password",
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "API token or Basic auth is required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "API token or Basic auth is required",
                    }
                }
            },
        },
    },
)
def add_movie(
    movie_create: MovieCreate,
) -> Movie:
    return storage.create(movie_create)
