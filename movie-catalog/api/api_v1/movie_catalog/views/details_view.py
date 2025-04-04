from typing import Annotated

from fastapi import APIRouter, Depends, status

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import prefetch_film
from schemas.movie_catalog import Movie

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
        }
    },
)


@router.get("/", response_model=Movie)
def get_movie(movie: Annotated[Movie, Depends(prefetch_film)]) -> Movie:
    return movie


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
def delete_movie(movie: Annotated[Movie, Depends(prefetch_film)]) -> None:
    storage.delete(movie)
