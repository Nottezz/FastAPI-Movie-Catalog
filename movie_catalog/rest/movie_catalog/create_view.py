from dependencies.movie_catalog import GetMovieCatalogStorage
from exceptions import MovieAlreadyExists
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError
from schemas.movie_catalog import MovieCreate
from services.movie_catalog.form_response_helper import FormResponseHelper

router = APIRouter(
    prefix="/create",
)

form_response = FormResponseHelper(
    model=MovieCreate,
    template_name="movie-catalog/create.html",
)


@router.get("/", name="movie-catalog:create-view")
def get_page_add_movie_to_catalog(request: Request) -> HTMLResponse:
    return form_response.render(request)


@router.post("/", name="movie-catalog:create", response_model=None)
async def add_movie(
    request: Request, storage: GetMovieCatalogStorage
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            movie_create = MovieCreate.model_validate(form)
        except ValidationError as e:
            return form_response.render(
                request=request,
                form_data=form,
                pydantic_error=e,
                form_validated=True,
            )

    try:
        storage.create_or_rise_if_exists(movie_create)
    except MovieAlreadyExists:
        errors = {
            "slug": f"Movie with slug '{movie_create.slug}' already exists.",
        }
    else:
        return RedirectResponse(
            url=request.url_for("movie-catalog:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )
    return form_response.render(
        request=request,
        errors=errors,
        form_data=movie_create,
        form_validated=True,
    )
