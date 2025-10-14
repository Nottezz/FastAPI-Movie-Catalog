from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from movie_catalog.config import settings
from movie_catalog.storage.movie_catalog import MovieCatalogStorage


@asynccontextmanager
async def lifespan(
    app: FastAPI,  # noqa: ARG001
) -> AsyncIterator[None]:
    app.state.movie_catalog_storage = MovieCatalogStorage(
        hast_name=settings.redis.collections.movie_catalog_hash,
    )
    yield
