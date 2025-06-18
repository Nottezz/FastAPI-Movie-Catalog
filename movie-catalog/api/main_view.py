from fastapi import APIRouter, Request

router = APIRouter()


@router.get("/")
def root(
    request: Request,
) -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs_url": str(docs_url),
    }
