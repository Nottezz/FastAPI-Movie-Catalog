from typing import Any

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from movie_catalog.dependencies.movie_catalog import GetMovieCatalogStorage
from movie_catalog.templating import templates

router = APIRouter()


@router.get("/", name="movie-catalog:list")
def list_view(request: Request, storage: GetMovieCatalogStorage) -> HTMLResponse:
    context: dict[str, Any] = {}
    movie_catalog = storage.get()
    context.update(movie_catalog=movie_catalog)
    return templates.TemplateResponse(
        request=request,
        name="movie-catalog/list.html",
        context=context,
    )
