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


def create_movie() -> Movie:
    movie_create = MovieCreate(slug="".join(random.choices(string.ascii_letters, k=10, ), ), title="Some title",
                               description="Some description for unit-test", year_released=1901, rating=1.0, )
    return storage.create(movie_create)


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie()
    yield movie
    storage.delete(movie)
