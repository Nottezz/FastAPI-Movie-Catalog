import pytest
from fastapi import status
from fastapi.testclient import TestClient


@pytest.mark.templatetest
def test_root(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.template.name == "home.html"  # type: ignore[attr-defined]
    assert "features" in response.context, response.context  # type: ignore[attr-defined]
    assert isinstance(response.context["features"], dict)  # type: ignore[attr-defined]


@pytest.mark.templatetest
def test_about(client: TestClient) -> None:
    response = client.get("/about")
    assert response.status_code == status.HTTP_200_OK
    assert response.template.name == "about.html"  # type: ignore[attr-defined]
    assert "today" in response.context, response.context  # type: ignore[attr-defined]
