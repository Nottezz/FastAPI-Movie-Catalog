from unittest import TestCase

from schemas.movie_catalog import MovieCreate, MovieUpdate, MoviePartialUpdate, Movie


class MovieCreateTestCase(TestCase):
    def test_movie_create_can_be_created_from_create_schema(self) -> None:
        movie_in = MovieCreate(
            slug="some-slug",
            title="Some title",
            description="Some description for unit-test",
            year_released=1901,
            rating=1.0,
        )

        movie = Movie(**movie_in.model_dump())

        self.assertEqual(movie_in.slug, movie.slug)
        self.assertEqual(movie_in.title, movie.title)
        self.assertEqual(movie_in.description, movie.description)
        self.assertEqual(movie_in.year_released, movie.year_released)
        self.assertEqual(movie_in.rating, movie.rating)


class MovieUpdateTestCase(TestCase):
    def test_movie_update_can_be_updated_from_update_schema(self) -> None:
        movie = Movie(
            slug="some-slug",
            title="Some title",
            description="Some description for unit-test",
            year_released=1901,
            rating=1.0,
        )

        movie_update = MovieUpdate(
            title="Some title from update schema",
            description="Some description for unit-test from update schema",
            year_released=2001,
            rating=10.0,
        )

        for field, value in movie_update:
            setattr(movie, field, value)

        self.assertEqual(movie_update.title, movie.title)
        self.assertEqual(movie_update.description, movie.description)
        self.assertEqual(movie_update.year_released, movie.year_released)
        self.assertEqual(movie_update.rating, movie.rating)


class MoviePartialUpdateTestCase(TestCase):
    def test_movie_partial_update_can_be_updated_from_partial_update_schema(
        self,
    ) -> None:
        movie = Movie(
            slug="some-slug",
            title="Some title",
            description="Some description for unit-test",
            year_released=1901,
            rating=1.0,
        )

        movie_partial_update = MoviePartialUpdate(
            title="Some title from partial update schema",
            year_released=2001,
        )

        for field, value in movie_partial_update.model_dump(exclude_unset=True).items():
            setattr(movie, field, value)

        self.assertEqual(movie_partial_update.title, movie.title)
        self.assertEqual(movie_partial_update.year_released, movie.year_released)
