from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(
    app: FastAPI,  # noqa: ARG001
) -> AsyncIterator[None]:

    yield
