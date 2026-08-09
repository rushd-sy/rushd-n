import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    db_file = tmp_path / "authors.json"
    db_file.write_text("[]", encoding="utf-8")

    return db_file


@pytest.fixture
def client(test_db):
    return TestClient(app)

def test_create_author(client):
    response = client.post("/authors", json={"name": "John Doe", "birth_year": 1990}, headers={"X-User-Id": "1"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["birth_year"] == 1990
    assert "author_id" in data


@pytest.mark.parametrize("invalid_input", [
    {"name": "", "birth_year": 1980},
    {"name": "Jane Doe", "birth_year": -1}, 
    {"name": "John Doe"},
    {"birth_year": 1990},
    {},
])
def test_create_author_invalid_input(client, invalid_input):
    response = client.post("/authors", json=invalid_input)
    assert response.status_code == 422


def test_update_author_not_found(client):
    response = client.put("/authors/999", json={"name": "Jane Doe", "birth_year": 1990})
    assert response.status_code == 403