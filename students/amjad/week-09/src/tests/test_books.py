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
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "mooo"
    assert data["author"] == "maaa"
    assert data["genre"] == "yooo"
    assert data["year"] == 1925
    assert "book_id" in data


@pytest.mark.parametrize(
    "invalid_input",
    [
        {
            "title": "",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        {"title": "mooo", "author": "", "genre": "yooo", "year": 1925},
        {
            "title": "mooo",
            "author": "maaa",
            "genre": "",
            "year": 1925,
        },
        {
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": -1,
        },
        {"title": "mooo", "author": "maaa", "year": 1925},
    ],
)
def test_create_book_invalid_input(client, invalid_input):
    response = client.post("/books", json=invalid_input)
    assert response.status_code == 422


def test_update_book_not_found(client):
    response = client.put(
        "/books/999",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 404
    assert response.json() == {"message": "Book 999 not found"}


def test_unauthorized_access(client):
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "unauthorized"}

def test_delete_book(client):
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    response = client.delete(f"/books/{book_id}", headers={"X-User-Id": "1"})
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["title"] == "mooo"
    assert data["author"] == "maaa"
    assert data["genre"] == "yooo"
    assert data["year"] == 1925

def test_update_book(client):
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["title"] == "mooo"
    assert data["author"] == "maaa"
    assert data["genre"] == "yooo"
    assert data["year"] == 1925