import logging
import random
import string
from os import getenv
from typing import Generator

import pytest

from api.api_v1.movie_catalog.crud import storage
from schemas.movie_catalog import Movie, MovieCreate

if getenv("TESTING") != "1":
    pytest.exit(
        "Environment is not ready for testing",
    )


@pytest.fixture(autouse=True)
def disable_logging():
    logging.getLogger().setLevel(logging.CRITICAL)


def build_movie_create(slug: str) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        title="Some title",
        description="Some description for unit-test",
        year_released=1901,
        rating=1.0,
    )


def build_movie_create_random_slug() -> MovieCreate:
    return MovieCreate(
        slug="".join(
            random.choices(
                string.ascii_letters,
                k=10,
            ),
        ),
        title="Some title",
        description="Some description for unit-test",
        year_released=1901,
        rating=1.0,
    )


def create_movie(slug: str) -> Movie:
    return storage.create(build_movie_create(slug))


def create_movie_random_slug() -> Movie:
    return storage.create(build_movie_create_random_slug())


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
