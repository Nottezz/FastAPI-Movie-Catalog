__all__ = ("router",)

from exceptions import MovieAlreadyExists
from fastapi import APIRouter, Depends, HTTPException, status

from movie_catalog.api.api_v1.movie_catalog.dependencies import (
    api_token_or_user_basic_auth_required,
)
from movie_catalog.schemas.movie_catalog import Movie, MovieCreate, MovieRead
from movie_catalog.storage.movie_catalog.crud import (
    storage,
)

router: APIRouter = APIRouter(
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
                        "detail": "Invalid API token or username and password.",
                    }
                }
            },
        },
        status.HTTP_403_FORBIDDEN: {
            "description": "API token or Basic auth is required",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "API token or Basic auth is required.",
                    }
                }
            },
        },
        status.HTTP_409_CONFLICT: {
            "description": "A movie with such slug already exists",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie with slug <name> already exists.",
                    }
                }
            },
        },
    },
)
def add_movie(
    movie_create: MovieCreate,
) -> Movie:
    try:
        return storage.create_or_rise_if_exists(movie_create)
    except MovieAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Movie with slug <{movie_create.slug}> already exists.",
        )
