import pytest


@pytest.mark.apitest
def test_root_view(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World",
        "docs_url": "http://testserver/docs",
    }
