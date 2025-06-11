import string
from os import getenv
from unittest import TestCase

from api.api_v1.movie_catalog.crud import storage
from schemas.movie_catalog import Movie, MovieCreate, MovieUpdate, MoviePartialUpdate

if getenv("TESTING") != "1":
    raise OSError(
        "Environment is not ready for testing",
    )


class MovieCatalogStorageTestCase(TestCase):
    def setUp(self):
        self.movie = self.create_movie()

    def create_movie(self) -> Movie:
        import random

        movie_in = MovieCreate(
            slug="".join(random.choices(string.ascii_letters + string.digits, k=8)),
            title="Some title",
            description="Some description for unit-test",
            year_released=1901,
            rating=1.0,
        )
        return storage.create(movie_in)

    def test_update_movie(self):
        source_description = self.movie.description

        movie_update = MovieUpdate(**self.movie.model_dump())
        movie_update.description *= 3
        updated_short_url = storage.update(movie=self.movie, updated_movie=movie_update)

        self.assertNotEqual(source_description, updated_short_url.description)
        self.assertEqual(movie_update, MovieUpdate(**updated_short_url.model_dump()))
        self.assertEqual(movie_update.description, updated_short_url.description)

    def test_partial_update_movie(self):
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

    def tearDown(self):
        storage.delete(self.movie)
