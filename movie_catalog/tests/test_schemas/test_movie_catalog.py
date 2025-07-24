from unittest import TestCase

from pydantic import ValidationError
from schemas.movie_catalog import Movie, MovieCreate, MoviePartialUpdate, MovieUpdate


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

    def test_movie_create_validate_value_at_fields(self) -> None:
        max_symbols_title = "Lorem ipsum dolor sit amet,consectetur adipiscing."
        max_symbols_desc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras erat diam, consectetur id eros non, pellentesque scelerisque sem. Curabitur vel tellus nisl. Aliquam in elit augue. Aliquam mattis pellentesque nisl eu tincidunt. Phasellus vitae quam felis. Integer tellus magna, tristique non commodo eu, venenatis ut nunc. Pellentesque ac enim sem. Nam luctus dapibus iaculis. Vestibulum sed posuere ante. Suspendisse condimentum, nunc et lobortis pretium, turpis dui malesuada enim, vitae porta metus. "

        movie_in_list = [
            MovieCreate(
                slug="some-slug",
                title="Some title",
                description="Some description for unit-test",
                year_released=1901,
                rating=1.0,
            ),
            MovieCreate(
                slug="some-slug",
                title=max_symbols_title,
                description=max_symbols_desc,
                year_released=9999,
                rating=10.0,
            ),
        ]
        for movie_in in movie_in_list:
            with self.subTest(movie_in=movie_in, msg=f"test-movie_in-{movie_in.title}"):
                movie = Movie(**movie_in.model_dump())

                self.assertEqual(movie_in.slug, movie.slug)
                self.assertEqual(movie_in.title, movie.title)
                self.assertEqual(movie_in.description, movie.description)
                self.assertEqual(movie_in.year_released, movie.year_released)
                self.assertEqual(movie_in.rating, movie.rating)

    def test_movie_slug_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="s",
                title="Some title",
                description="Some description for unit-test",
                year_released=1901,
                rating=1.0,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(expected_type, error_details["type"])

    def test_movie_title_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="some-slug",
                title="S",
                description="Some description for unit-test",
                year_released=1901,
                rating=1.0,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(expected_type, error_details["type"])

    def test_movie_description_too_short(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="some-slug",
                title="Some title",
                description="S",
                year_released=1901,
                rating=1.0,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "string_too_short"
        self.assertEqual(expected_type, error_details["type"])

    def test_movie_year_released_less_than_1901(self) -> None:
        with self.assertRaises(ValidationError) as exc_info:
            MovieCreate(
                slug="some-slug",
                title="Some title",
                description="Some description for unit-test",
                year_released=1899,
                rating=1.0,
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "greater_than_equal"
        self.assertEqual(expected_type, error_details["type"])

    def test_movie_rating_less(self) -> None:
        with self.assertRaisesRegex(
            ValidationError, expected_regex="Input should be greater than or equal to 0"
        ) as exc_info:
            MovieCreate(
                slug="some-slug",
                title="Some title",
                description="Some description for unit-test",
                year_released=1901,
                rating=float(-1.2),
            )

        error_details = exc_info.exception.errors()[0]
        expected_type = "greater_than_equal"
        self.assertEqual(expected_type, error_details["type"])


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
