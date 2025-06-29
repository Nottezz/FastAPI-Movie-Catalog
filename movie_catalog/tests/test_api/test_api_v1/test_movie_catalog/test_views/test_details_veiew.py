from typing import Generator

import pytest
from fastapi import status

from api.api_v1.movie_catalog.crud import storage
from main import app
from schemas.movie_catalog import Movie, DESCRIPTION_MIN_LENGTH, DESCRIPTION_MAX_LENGTH
from tests.conftest import create_movie, create_movie_random_slug


class TestDelete:
    @pytest.fixture(
        params=[
            "some-slug",
            "slug",
            pytest.param("abc", id="minimal-slug"),
            pytest.param(
                "abc-qwe-qwerty-some-slug-abc-qwe-qwerty-some-slugg", id="max-slug"
            ),
        ]
    )
    def movie(self, request) -> Generator[Movie, None, None]:
        movie = create_movie(slug=request.param)
        yield movie
        storage.delete(movie)

    def test_delete_movie(self, movie, auth_client) -> None:
        url = app.url_path_for("delete_movie", slug=movie.slug)
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
        assert not storage.exists(movie.slug)


class TestPartialUpdate:
    @pytest.fixture()
    def movie(self, request) -> Generator[Movie, None, None]:
        movie = create_movie_random_slug(description=request.param)
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description",
        [
            pytest.param("a" * 23, "a" * 100, id="mid-desc-to-large-desc"),
            pytest.param(
                "a" * DESCRIPTION_MAX_LENGTH,
                "a" * DESCRIPTION_MIN_LENGTH,
                id="max-desc-to-min-desc",
            ),
            pytest.param(
                "a" * DESCRIPTION_MIN_LENGTH,
                "a" * DESCRIPTION_MAX_LENGTH,
                id="max-desc-to-no-desc",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details_partial(
        self, movie, auth_client, new_description
    ) -> None:
        url = app.url_path_for("partial_update_movie", slug=movie.slug)
        movie_before_update = storage.get_by_slug(movie.slug)
        response = auth_client.patch(url, json={"description": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_from_db = storage.get_by_slug(movie.slug)
        assert movie_from_db != movie_before_update
        assert movie_from_db.description == new_description
