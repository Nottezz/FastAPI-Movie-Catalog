from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import (
    api_token_or_user_basic_auth_required,
    prefetch_film,
)
from schemas.movie_catalog import Movie, MoviePartialUpdate, MovieRead, MovieUpdate

router = APIRouter(
    prefix="/{slug}",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'slug' not found.",
                    }
                }
            },
        },
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
    },
)

MovieBySlug = Annotated[Movie, Depends(prefetch_film)]


@router.get("/", response_model=MovieRead)
def get_movie(movie: MovieBySlug) -> Movie:
    return movie


@router.put(
    "/",
    response_model=MovieRead,
    dependencies=[
        Depends(api_token_or_user_basic_auth_required),
    ],
)
def update_movie(
    movie: MovieBySlug,
    movie_updated: MovieUpdate,
) -> Movie:
    return storage.update(movie, movie_updated)


@router.patch(
    "/",
    response_model=MovieRead,
    dependencies=[
        Depends(api_token_or_user_basic_auth_required),
    ],
)
def partial_update_movie(
    movie: MovieBySlug,
    movie_partial: MoviePartialUpdate,
) -> Movie:
    return storage.partial_update(movie, movie_partial)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(api_token_or_user_basic_auth_required),
    ],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Movie not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Movie 'slug' not found",
                    }
                }
            },
        }
    },
)
def delete_movie(
    movie: MovieBySlug,
) -> None:
    storage.delete(movie)
