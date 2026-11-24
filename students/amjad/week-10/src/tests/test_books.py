from typing import Any
import pytest
from fastapi.testclient import TestClient


def test_create_book(
    client: TestClient, auth_headers: dict[str, str], create_author: dict[str, Any]
) -> None:
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author_id": create_author["author_id"],
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "mooo"
    assert data["author_id"] == create_author["author_id"]
    assert data["genre"] == "yooo"
    assert data["year"] == 1925
    assert "book_id" in data


@pytest.mark.parametrize(
    "invalid_input",
    [
        {
            "title": "",
            "author_id": 1,
            "genre": "yooo",
            "year": 1925,
        },
        {"title": "mooo", "author_id": 0, "genre": "yooo", "year": 1925},
        {
            "title": "mooo",
            "author_id": 1,
            "genre": "",
            "year": 1925,
        },
        {
            "title": "mooo",
            "author_id": 1,
            "genre": "yooo",
            "year": -1,
        },
        {"title": "mooo", "author_id": 1, "year": 1925},
    ],
)
def test_create_book_invalid_input(
    client: TestClient, invalid_input: dict[str, Any], auth_headers: dict[str, str]
) -> None:
    response = client.post("/books", json=invalid_input, headers=auth_headers)
    assert response.status_code == 422



def test_update_book_not_found(
    client: TestClient, auth_headers: dict[str, str], create_author: dict[str, Any]
) -> None:
    response = client.put(
        "/books/999",
        json={
            "title": "mooo",
            "author_id": create_author["author_id"],
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json() == {"message": "Book 999 not found"}


def test_unauthorized_access(client: TestClient, create_author: dict[str, Any]) -> None:
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author_id": create_author["author_id"],
            "genre": "yooo",
            "year": 1925,
        },
    )
    assert response.status_code == 401

def test_delete_book(
    client: TestClient, auth_headers: dict[str, str], create_author: dict[str, Any]
) -> None:
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author_id": create_author["author_id"],
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    response = client.delete(f"/books/{book_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["title"] == "mooo"
    assert data["author_id"] == create_author["author_id"]
    assert data["genre"] == "yooo"
    assert data["year"] == 1925

def test_update_book(
    client: TestClient, auth_headers: dict[str, str], create_author: dict[str, Any]
) -> None:
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author_id": create_author["author_id"],
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "mooo",
            "author_id": 1,
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["title"] == "mooo"
    assert data["author_id"] == create_author["author_id"]
    assert data["genre"] == "yooo"
    assert data["year"] == 1925

def test_create_book_with_nonexistent_author(
    client: TestClient, auth_headers: dict[str, str]
) -> None:
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author_id": 9999,
            "genre": "yooo",
            "year": 2000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "author not found"}

def test_update_book_with_nonexistent_author(
    client: TestClient, auth_headers: dict[str, str], create_author: dict[str, Any]
) -> None:
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author_id": create_author["author_id"],
            "genre": "yooo",
            "year": 2000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    book_id = response.json()["book_id"]

    response = client.put(
        f"/books/{book_id}",
        json={
            "title": "mooo",
            "author_id": 9999,
            "genre": "yooo",
            "year": 2000,
        },
        headers=auth_headers,
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "author not found"}