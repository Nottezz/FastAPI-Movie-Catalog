import random
import string

from fastapi.testclient import TestClient
from fastapi import status

from movie_catalog.main import app
from schemas.movie_catalog import MovieCreate, Movie


def test_create_movie(auth_client: TestClient):
    url = app.url_path_for("add_movie")
    movie_create = MovieCreate(slug="".join(random.choices(string.ascii_letters, k=10, ), ), title="Some title",
                         description="Some description for unit-test", year_released=1901, rating=1.0, )
    data = movie_create.model_dump(mode="json")
    response = auth_client.post(url, json=data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    received_data = MovieCreate(**response.json())
    assert received_data == movie_create, received_data

def test_create_movie_already_exists(auth_client: TestClient, movie: Movie):
    url = app.url_path_for("add_movie")
    movie_create = MovieCreate(**movie.model_dump())
    data = movie_create.model_dump(mode="json")
    response = auth_client.post(url, json=data)
    assert response.status_code == status.HTTP_409_CONFLICT, response.text
    response_data = response.json()
    expected_error_detail = f"Movie with slug <{movie.slug}> already exists."
    assert response_data["detail"] == expected_error_detail, response_data
