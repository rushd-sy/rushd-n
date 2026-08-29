import pytest


def test_create_author(client, auth_headers):
    response = client.post(
        "/authors",
        json={"name": "John Doe", "birth_year": 1990},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["birth_year"] == 1990
    assert "author_id" in data


@pytest.mark.parametrize(
    "invalid_input",
    [
        {"name": "", "birth_year": 1980},
        {"name": "Jane Doe", "birth_year": -1},
        {"name": "John Doe"},
        {"birth_year": 1990},
        {},
    ],
)
def test_create_author_invalid_input(client, invalid_input, auth_headers):
    response = client.post("/authors", json=invalid_input, headers=auth_headers)
    assert response.status_code == 422


def test_update_author_not_found(client, auth_headers):
    response = client.put(
        "/authors/999",
        json={"name": "Jane Doe", "birth_year": 1990},
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Author not found"}


def test_unauthorized_access(client):
    response = client.post("/authors", json={"name": "John Doe", "birth_year": 1990})
    assert response.status_code == 401

def test_delete_author(client, auth_headers):
    response = client.post(
        "/authors",
        json={"name": "John Doe", "birth_year": 1990},
        headers=auth_headers,
    )
    assert response.status_code == 200
    author_id = response.json()["author_id"]

    response = client.delete(f"/authors/{author_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["author_id"] == author_id
    assert data["name"] == "John Doe"
    assert data["birth_year"] == 1990

def test_update_author(client, auth_headers):
    response = client.post(
        "/authors",
        json={"name": "John Doe", "birth_year": 1990},
        headers=auth_headers,
    )
    assert response.status_code == 200
    author_id = response.json()["author_id"]

    response = client.put(
        f"/authors/{author_id}",
        json={"name": "Jane Doe", "birth_year": 1995},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["author_id"] == author_id
    assert data["name"] == "Jane Doe"
    assert data["birth_year"] == 1995