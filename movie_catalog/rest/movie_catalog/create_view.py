from typing import Any, Mapping

from dependencies.movie_catalog import GetMovieCatalogStorage
from exceptions import MovieAlreadyExists
from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, ValidationError
from schemas.movie_catalog import MovieCreate
from templating import templates

router = APIRouter(
    prefix="/create",
)


@router.get("/", name="movie-catalog:create-view")
def get_page_add_movie_to_catalog(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = MovieCreate.model_json_schema()
    context.update(model_schema=model_schema)
    return templates.TemplateResponse(  # type: ignore
        request=request,
        name="movie-catalog/create.html",
        context=context,
    )


def format_pydantic_errors(error: ValidationError) -> dict[str, str]:
    return {f"{err["loc"][0]}": err["msg"] for err in error.errors()}


def create_view_validation_response(
    request: Request,
    form_data: BaseModel | Mapping[str, Any] | None = None,
    errors: dict[str, str] | None = None,
    form_validated: bool = True,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = MovieCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
        form_data=form_data,
        errors=errors,
        form_validated=form_validated,
    )
    return templates.TemplateResponse(  # type: ignore
        request=request,
        name="movie-catalog/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@router.post("/", name="movie-catalog:create", response_model=None)
async def add_movie(
    request: Request, storage: GetMovieCatalogStorage
) -> RedirectResponse | HTMLResponse:
    async with request.form() as form:
        try:
            movie_create = MovieCreate.model_validate(form)
        except ValidationError as e:
            errors = format_pydantic_errors(e)
            return create_view_validation_response(
                request=request, errors=errors, form_data=form
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
    return create_view_validation_response(
        errors=errors, request=request, form_data=movie_create
    )
