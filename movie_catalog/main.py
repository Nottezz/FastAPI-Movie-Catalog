import logging

from fastapi import FastAPI

from movie_catalog.api import router as api_router
from movie_catalog.api.main_view import router as main_router
from movie_catalog.app_lifespan import lifespan
from movie_catalog.config import settings

logging.basicConfig(
    format=settings.logging.log_format,
    level=settings.logging.log_level,
    datefmt=settings.logging.log_date_format,
)

app = FastAPI(
    title="Movies",
    description="Movie catalog",
    version="1.0",
    lifespan=lifespan,
)
app.include_router(main_router)
app.include_router(api_router)
