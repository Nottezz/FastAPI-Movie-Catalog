from unittest import TestCase

from schemas.movie_catalog import MovieCreate, Movie


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
