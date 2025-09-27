from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from templating.jinja_templates import templates

router = APIRouter()


@router.get("/", include_in_schema=False, name="home")
def home_page(
    request: Request,
) -> HTMLResponse:
    return templates.TemplateResponse(request=request, name="home.html")
