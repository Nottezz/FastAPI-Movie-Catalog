import string
from typing import ClassVar
from unittest import TestCase

import pytest

from movie_catalog.exceptions import MovieAlreadyExists
from movie_catalog.schemas.movie_catalog import (
    Movie,
    MovieCreate,
    MoviePartialUpdate,
    MovieUpdate,
)
from movie_catalog.storage.movie_catalog.crud import (
    storage,
)
from movie_catalog.tests.conftest import build_movie_create_random_slug


def create_movie() -> Movie:
    import random

    movie_in = MovieCreate(
        slug="".join(
            random.choices(  # noqa: S311 Standard pseudo-random generators are not suitable for cryptographic purposes
                string.ascii_letters + string.digits, k=8
            )
        ),
        title="Some title",
        description="Some description for unit-test",
        year_released=1901,
        rating=1.0,
    )
    return storage.create(movie_in)


class MovieCatalogStorageTestCase(TestCase):
    def setUp(self) -> None:
        self.movie = create_movie()

    def test_update_movie(self) -> None:
        source_description = self.movie.description

        movie_update = MovieUpdate(**self.movie.model_dump())
        movie_update.description *= 3
        updated_short_url = storage.update(movie=self.movie, updated_movie=movie_update)

        self.assertNotEqual(source_description, updated_short_url.description)
        self.assertEqual(movie_update, MovieUpdate(**updated_short_url.model_dump()))
        self.assertEqual(movie_update.description, updated_short_url.description)

    def test_partial_update_movie(self) -> None:
        movie_partial_update = MoviePartialUpdate(
            description=self.movie.description * 2
        )
        source_description = self.movie.description
        partial_updated_movie = storage.partial_update(
            movie=self.movie, updated_movie=movie_partial_update
        )

        self.assertNotEqual(source_description, partial_updated_movie.description)
        self.assertEqual(
            movie_partial_update.description, partial_updated_movie.description
        )

    def tearDown(self) -> None:
        storage.delete(self.movie)


class MovieCatalogStorageGetMoviesTestCase(TestCase):
    MOVIES_COUNT = 5
    movies: ClassVar[list[Movie]] = []

    @classmethod
    def setUpClass(cls) -> None:
        cls.movies = [create_movie() for _ in range(cls.MOVIES_COUNT)]

    def test_get_movies_list(self) -> None:
        expected_slugs = {movie.slug for movie in self.movies}
        slugs = {movie.slug for movie in storage.get()}
        expected_diff = set[str]()
        diff = expected_slugs - slugs

        self.assertEqual(expected_diff, diff)

    def test_get_by_slug(self) -> None:
        for movie in self.movies:
            with self.subTest(
                slug=movie.slug, msg=f"Validate can get slug {movie.slug}"
            ):
                db_movie = storage.get_by_slug(slug=movie.slug)
                self.assertEqual(movie, db_movie)

    @classmethod
    def tearDownClass(cls) -> None:
        for movie in cls.movies:
            storage.delete(movie)


def test_create_or_raise_if_exists(movie: Movie) -> None:
    movie_create = MovieCreate(**movie.model_dump())
    with pytest.raises(MovieAlreadyExists, match=movie_create.slug) as exc_info:
        storage.create_or_rise_if_exists(movie_create)

    assert exc_info.value.args[0] == movie_create.slug


def test_create_twice() -> None:
    movie_create = build_movie_create_random_slug()
    storage.create_or_rise_if_exists(movie_create)
    with pytest.raises(MovieAlreadyExists, match=movie_create.slug) as exc_info:
        storage.create_or_rise_if_exists(movie_create)

    assert exc_info.value.args == (movie_create.slug,)
