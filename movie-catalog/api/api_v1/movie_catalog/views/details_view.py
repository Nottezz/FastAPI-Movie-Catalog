from typing import Annotated

from fastapi import APIRouter, Depends, status, BackgroundTasks

from api.api_v1.movie_catalog.crud import storage
from api.api_v1.movie_catalog.dependencies import prefetch_film
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
        }
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
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_storage)
    return storage.update(movie, movie_updated)


@router.patch("/", response_model=MovieRead)
def partial_update_movie(
    movie: MovieBySlug,
    movie_partial: MoviePartialUpdate,
    background_tasks: BackgroundTasks,
) -> Movie:
    background_tasks.add_task(storage.save_storage)
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
    background_tasks: BackgroundTasks,
) -> None:
    storage.delete(movie)
    background_tasks.add_task(storage.save_storage)
