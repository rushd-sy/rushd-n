import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    db_file = tmp_path / "books.json"
    db_file.write_text("[]", encoding="utf-8")

    return db_file


@pytest.fixture
def client(test_db):
    return TestClient(app)

def test_create_book(client):
    response = client.post("/books", json={"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "year": 1925}, headers={"X-User-Id": "1"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "The Great Gatsby"
    assert data["author"] == "F. Scott Fitzgerald"
    assert data["genre"] == "Fiction"
    assert data["year"] == 1925
    assert "book_id" in data


@pytest.mark.parametrize("invalid_input", [
    {"title": "", "author": "F. Scott Fitzgerald", "genre": "Fiction", "year": 1925},
    {"title": "The Great Gatsby", "author": "", "genre": "Fiction", "year": 1925},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "", "year": 1925},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "year": -1},
    {"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "year": 1925},
])
def test_create_book_invalid_input(client, invalid_input):
    response = client.post("/books", json=invalid_input)
    assert response.status_code == 422


def test_update_book_not_found(client):
    response = client.put("/books/999", json={"title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "genre": "Fiction", "year": 1925})
    assert response.status_code == 403