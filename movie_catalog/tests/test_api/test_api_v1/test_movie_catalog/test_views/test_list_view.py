import logging
import random
import string
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from movie_catalog.main import app
from schemas.movie_catalog import MovieCreate, Movie
from tests.conftest import build_movie_create_random_slug

pytestmark = pytest.mark.apitest


class TestCreate:
    def test_create_movie(self, caplog, auth_client: TestClient):

        caplog.set_level(logging.DEBUG)

        url = app.url_path_for("add_movie")
        movie_create = MovieCreate(
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
        data = movie_create.model_dump(mode="json")
        response = auth_client.post(url, json=data)
        assert response.status_code == status.HTTP_201_CREATED, response.text
        received_data = MovieCreate(**response.json())
        assert received_data == movie_create, received_data
        assert f"Add movie <{received_data.slug}> to catalog" in caplog.text

    def test_create_movie_already_exists(self, auth_client: TestClient, movie: Movie):
        url = app.url_path_for("add_movie")
        movie_create = MovieCreate(**movie.model_dump())
        data = movie_create.model_dump(mode="json")
        response = auth_client.post(url, json=data)
        assert response.status_code == status.HTTP_409_CONFLICT, response.text
        response_data = response.json()
        expected_error_detail = f"Movie with slug <{movie.slug}> already exists."
        assert response_data["detail"] == expected_error_detail, response_data


class TestCreateInvalid:
    @pytest.fixture(
        params=[
            pytest.param(("a", "string_too_short"), id="too_short"),
            pytest.param(
                (
                    "abc-qwe-qwerty-some-slug-abc-qwe-qwerty-some-sluggg",
                    "string_too_long",
                ),
                id="too_long",
            ),
        ]
    )
    def movie_create_values(self, request) -> tuple[dict[str, Any], str]:
        build = build_movie_create_random_slug()
        data = build.model_dump(mode="json")
        slug, err_type = request.param
        data["slug"] = slug
        return data, err_type

    def test_invalid_slug(self, auth_client, movie_create_values):
        url = app.url_path_for("add_movie")
        created_data, expected_error_type = movie_create_values
        response = auth_client.post(url, json=created_data)
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
        error_detail = response.json()["detail"][0]
        assert error_detail["type"] == expected_error_type, error_detail
