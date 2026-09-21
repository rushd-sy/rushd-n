import pytest


def test_create_book(client, auth_headers):
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
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
def test_create_book_invalid_input(client, invalid_input, auth_headers):
    response = client.post("/books", json=invalid_input, headers=auth_headers)
    assert response.status_code == 422


def test_update_book_not_found(client, auth_headers):
    response = client.put(
        "/books/999",
        json={
            "title": "mooo",
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
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

def test_delete_book(client, auth_headers):
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
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
    assert data["author"] == "maaa"
    assert data["genre"] == "yooo"
    assert data["year"] == 1925

def test_update_book(client, auth_headers):
    response = client.post(
        "/books",
        json={
            "title": "mooo",
            "author": "maaa",
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
            "author": "maaa",
            "genre": "yooo",
            "year": 1925,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == book_id
    assert data["title"] == "mooo"
    assert data["author"] == "maaa"
    assert data["genre"] == "yooo"
    assert data["year"] == 1925