import logging

from fastapi import FastAPI, Request

import config
from api import router as api_router
from app_lifespan import lifespan

logging.basicConfig(
    format=config.LOG_FORMAT,
    level=config.LOG_LEVEL,
)

app = FastAPI(
    title="Movies",
    description="Movie catalog",
    version="1.0",
    lifespan=lifespan,
)
app.include_router(api_router)


@app.get("/")
def root(
    request: Request,
) -> dict[str, str]:
    docs_url = request.url.replace(path="/docs")
    return {
        "message": "Hello World",
        "docs_url": str(docs_url),
    }
