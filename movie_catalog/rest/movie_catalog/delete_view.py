import logging

from dependencies.movie_catalog import GetMovieCatalogStorage, MovieBySlug
from fastapi import APIRouter, Request, Response, status
from misc.flash_messages import flash
from starlette.requests import Request

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
