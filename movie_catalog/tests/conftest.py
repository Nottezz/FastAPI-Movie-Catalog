import logging
import random
import string
from os import getenv
from typing import Generator

import pytest
from schemas.movie_catalog import Movie, MovieCreate

from movie_catalog.api.api_v1.movie_catalog.crud import storage


@pytest.fixture(scope="session", autouse=True)
def check_testing_env() -> None:
    if getenv("TESTING") != "1":
        pytest.exit(
            "Environment is not ready for testing",
        )


@pytest.fixture(autouse=True)
def disable_logging() -> None:
    logging.getLogger().setLevel(logging.CRITICAL)


def build_movie_create(
    slug: str,
    description: str = "Some description for unit-test",
    title: str = "Some title",
) -> MovieCreate:
    return MovieCreate(
        slug=slug,
        title=title,
        description=description,
        year_released=1901,
        rating=1.0,
    )


def build_movie_create_random_slug(
    description: str = "Some description for unit-test",
    title: str = "Some title",
) -> MovieCreate:
    return MovieCreate(
        slug="".join(
            random.choices(  # noqa:  S311 Standard pseudo-random generators are not suitable for cryptographic purposes
                string.ascii_letters,
                k=10,
            ),
        ),
        title=title,
        description=description,
        year_released=1901,
        rating=1.0,
    )


def create_movie(
    slug: str,
    description: str = "Some description for unit-test",
    title: str = "Some title",
) -> Movie:
    return storage.create(build_movie_create(slug, description, title))


def create_movie_random_slug(
    description: str = "Some description for unit-test",
    title: str = "Some title",
) -> Movie:
    return storage.create(build_movie_create_random_slug(description, title))


@pytest.fixture()
def movie() -> Generator[Movie, None, None]:
    movie = create_movie_random_slug()
    yield movie
    storage.delete(movie)
