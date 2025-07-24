from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from api.api_v1.movie_catalog.crud import storage
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from schemas.movie_catalog import (
    DESCRIPTION_MAX_LENGTH,
    DESCRIPTION_MIN_LENGTH,
    Movie,
    MovieUpdate,
)

from tests.conftest import create_movie, create_movie_random_slug

pytestmark = pytest.mark.apitest


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
    def movie(self, request: SubRequest) -> Generator[Movie, None, None]:
        movie = create_movie(slug=request.param)
        yield movie
        storage.delete(movie)

    def test_delete_movie(self, movie: Movie, auth_client: TestClient) -> None:
        url = app.url_path_for("delete_movie", slug=movie.slug)
        response = auth_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
        assert not storage.exists(movie.slug)


class TestPartialUpdate:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie, None, None]:
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
        self,
        movie: Movie,
        auth_client: TestClient,
        new_description: str,
    ) -> None:
        url = app.url_path_for("partial_update_movie", slug=movie.slug)
        movie_before_update = storage.get_by_slug(movie.slug)
        response = auth_client.patch(url, json={"description": new_description})
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_from_db = storage.get_by_slug(movie.slug)
        assert movie_from_db != movie_before_update
        assert movie_from_db.description == new_description


class TestUpdate:
    @pytest.fixture()
    def movie(self, request: SubRequest) -> Generator[Movie, None, None]:
        description, title = request.param
        movie = create_movie_random_slug(description=description, title=title)
        yield movie
        storage.delete(movie)

    @pytest.mark.parametrize(
        "movie, new_description, new_title",
        [
            pytest.param(
                ("a" * DESCRIPTION_MIN_LENGTH, "abc"),
                "a" * 50,
                "Human Message from Space",
                id="min-description-and-title",
            ),
            pytest.param(
                ("a" * DESCRIPTION_MAX_LENGTH, "a" * 50),
                "a" * DESCRIPTION_MIN_LENGTH,
                "UFOs in the sky!",
                id="max-description-and-title",
            ),
            pytest.param(
                (
                    "abc-qwe-qwerty-some-slug-abc-qwe-qwerty-some-slugg-qwe-abc",
                    "Some Title",
                ),
                "a" * 50,
                "Human Message from Space",
                id="default-description-and-title",
            ),
        ],
        indirect=["movie"],
    )
    def test_update_movie_details(
        self,
        movie: Movie,
        auth_client: TestClient,
        new_description: str,
        new_title: str,
    ) -> None:
        url = app.url_path_for("update_movie", slug=movie.slug)
        movie_before_update = storage.get_by_slug(movie.slug)
        movie_update = MovieUpdate(
            description=new_description,
            title=new_title,
            year_released=1992,
            rating=10.0,
        ).model_dump(mode="json")

        response = auth_client.put(url, json=movie_update)
        assert response.status_code == status.HTTP_200_OK, response.text
        movie_from_db = storage.get_by_slug(movie.slug)
        assert movie_from_db != movie_before_update
        assert movie_from_db.description == new_description
        assert movie_from_db.title == new_title
