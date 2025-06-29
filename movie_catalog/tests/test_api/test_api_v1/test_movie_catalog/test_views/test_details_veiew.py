from typing import Generator

import pytest
from fastapi import status

from api.api_v1.movie_catalog.crud import storage
from main import app
from schemas.movie_catalog import Movie
from tests.conftest import create_movie


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
def movie(request) -> Generator[Movie, None, None]:
    movie = create_movie(slug=request.param)
    yield movie
    storage.delete(movie)


def test_delete_movie(movie, auth_client) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
