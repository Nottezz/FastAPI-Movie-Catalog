from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from movie_catalog.dependencies.movie_catalog import GetMovieCatalogStorage, MovieBySlug
from movie_catalog.misc.flash_messages import flash
from movie_catalog.schemas.movie_catalog import MovieUpdate
from movie_catalog.services.movie_catalog.form_response_helper import FormResponseHelper

router = APIRouter(
    prefix="/{slug}/update",
)

form_response = FormResponseHelper(
    model=MovieUpdate,
    template_name="movie-catalog/update.html",
)


@router.get("/", name="movie-catalog:update-view")
def get_page_update_movie_to_catalog(
    request: Request,
    movie: MovieBySlug,
) -> HTMLResponse:
    form = MovieUpdate(**movie.model_dump())
    return form_response.render(
        request,
        form_data=form,
        movie=movie,
    )


@router.post("/", name="movie-catalog:update", response_model=None)
async def update_movie(
    request: Request,
    movie: MovieBySlug,
    storage: GetMovieCatalogStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            movie_update = MovieUpdate.model_validate(form)
        except ValidationError as e:
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=e,
                form_validated=True,
                movie=movie,
            )

    storage.update(movie, movie_update)
    flash(
        request=request,
        message=f"Movie {movie_update.title!r} has been updated.",
        category="success",
    )
    return RedirectResponse(
        url=request.url_for("movie-catalog:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
