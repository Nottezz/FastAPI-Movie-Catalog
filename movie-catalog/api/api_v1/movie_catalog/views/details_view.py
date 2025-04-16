from typing import Annotated

from fastapi import APIRouter, Depends, status, BackgroundTasks

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import prefetch_film, validate_api_token
from schemas.movie_catalog import Movie, MovieUpdate, MoviePartialUpdate, MovieRead

router = APIRouter(
    prefix="/{slug}",
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
        },
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

MovieBySlug = Annotated[Movie, Depends(prefetch_film)]


@router.get("/", response_model=MovieRead)
def get_movie(movie: MovieBySlug) -> Movie:
    return movie


@router.put("/", response_model=MovieRead)
def update_movie(
    movie: MovieBySlug,
    movie_updated: MovieUpdate,
    _=Depends(validate_api_token),
) -> Movie:
    return storage.update(movie, movie_updated)


@router.patch("/", response_model=MovieRead)
def partial_update_movie(
    movie: MovieBySlug,
    movie_partial: MoviePartialUpdate,
    _=Depends(validate_api_token),
) -> Movie:
    return storage.partial_update(movie, movie_partial)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
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
    _=Depends(validate_api_token),
) -> None:
    storage.delete(movie)
