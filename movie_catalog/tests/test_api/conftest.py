from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from movie_catalog.main import app


@pytest.fixture()
def client() -> Generator[TestClient]:
    with TestClient(app) as client:
        yield client