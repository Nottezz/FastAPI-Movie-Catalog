from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(
    prefix="/{slug}/delete",
)


@router.post("/", name="movie-catalog:delete", response_model=None)
async def delete_movie(request: Request) -> RedirectResponse | HTMLResponse:
    return RedirectResponse(
        url=request.url_for("movie-catalog:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
