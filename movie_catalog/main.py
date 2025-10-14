import logging

from fastapi import FastAPI
from rest import router as rest_router
from starlette.middleware.sessions import SessionMiddleware

from movie_catalog.api import router as api_router
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
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session.secret_key,
)
app.include_router(rest_router)
app.include_router(api_router)
