from datetime import date

from config import BASE_DIR
from fastapi import Request
from fastapi.templating import Jinja2Templates


def inject_current_date(
    request: Request,  # noqa: ARG001 Unused function argument: `request`
) -> dict[str, date]:
    return {"today": date.today()}


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[
        inject_current_date,
    ],
)
