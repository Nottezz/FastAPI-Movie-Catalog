import pytest

from api.api_v1.movie_catalog.crud import storage
from main import app
from schemas.movie_catalog import MovieCreate, Movie

from fastapi import status


def create_movie(slug: str) -> Movie:
    movie_create = MovieCreate(
        slug=slug,
        title="Some title",
        description="Some description for unit-test",
        year_released=1901,
        rating=1.0,
    )
    return storage.create(movie_create)


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
def movie(request) -> Movie:
    return create_movie(slug=request.param)


def test_delete_movie(movie, auth_client) -> None:
    url = app.url_path_for("delete_movie", slug=movie.slug)
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text
    assert not storage.exists(movie.slug)
