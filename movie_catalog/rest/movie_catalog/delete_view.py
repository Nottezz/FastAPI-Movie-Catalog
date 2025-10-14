import logging

from dependencies.movie_catalog import GetMovieCatalogStorage, MovieBySlug
from fastapi import APIRouter, Response, status

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/{slug}/delete",
)


@router.delete("/", name="movie-catalog:delete", response_model=None)
async def delete_movie(
    movie: MovieBySlug,
    storage: GetMovieCatalogStorage,
) -> Response:
    storage.delete(movie)
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
