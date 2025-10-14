import logging

from dependencies.movie_catalog import GetMovieCatalogStorage, MovieBySlug
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/{slug}/delete",
)


@router.post("/", name="movie-catalog:delete", response_model=None)
async def delete_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMovieCatalogStorage,
) -> RedirectResponse | HTMLResponse:
    storage.delete(movie)
    return RedirectResponse(
        url=request.url_for("movie-catalog:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
