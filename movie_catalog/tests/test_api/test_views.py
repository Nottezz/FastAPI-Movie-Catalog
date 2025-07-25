import pytest
from fastapi.testclient import TestClient


@pytest.mark.apitest
def test_root_view(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World",
        "docs_url": "http://testserver/docs",
    }
