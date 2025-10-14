import logging

from fastapi import APIRouter, Request, Response, status
from starlette.requests import Request

from movie_catalog.dependencies.movie_catalog import GetMovieCatalogStorage, MovieBySlug
from movie_catalog.misc.flash_messages import flash

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/{slug}/delete",
)


@router.delete("/", name="movie-catalog:delete", response_model=None)
async def delete_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMovieCatalogStorage,
) -> Response:
    storage.delete(movie)
    flash(
        request=request,
        message=f"Movie {movie.title!r} has been deleted.",
        category="danger",
    )
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
