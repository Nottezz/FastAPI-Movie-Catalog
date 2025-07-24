import logging

from fastapi import FastAPI

from movie_catalog import config
from movie_catalog.api import router as api_router
from movie_catalog.api.main_view import router as main_router
from movie_catalog.app_lifespan import lifespan

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
app.include_router(main_router)
app.include_router(api_router)
