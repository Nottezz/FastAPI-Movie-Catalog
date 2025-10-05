from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from templating.jinja_templates import templates

router = APIRouter()


@router.get("/", include_in_schema=False, name="home")
def home_page(
    request: Request,
) -> HTMLResponse:

    context: dict[str, Any] = {}
    features = {
        "🚀 Fast API": "High performance with automatic OpenAPI documentation generation.",
        "⭐ Movie Ratings": "Rate movies and build your own catalog of the best ones.",
        "️🛠️ Easy Integration": "Clean and simple codebase that is easy to extend and improve.",
    }
    context.update(
        features=features,
    )
    return templates.TemplateResponse(  # type: ignore[no-any-return]
        request=request, name="home.html", context=context
    )


@router.get("/about", include_in_schema=False, name="about")
def about_page(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="about.html")  # type: ignore[no-any-return]
