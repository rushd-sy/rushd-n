import pytest
from fastapi.testclient import TestClient
from datetime import date
import json

from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def temp_authors_db(tmp_path, monkeypatch):
    authros_file = tmp_path / "authors_test.json"
    monkeypatch.setattr("utils.storage.AUTHORS_FILE", authros_file)

    fake_authors_json = [
        {    
            "author_id": 1,
            "name": "Bitar",
            "birth_year": 2005,
            "added_at": date.today().isoformat(),
        }, 
        {
            "author_id": 2,
            "name": "Bakro",
            "birth_year": 2005,
            "added_at": date.today().isoformat(),    
        }
    ]
    
    with open(authros_file, 'w') as file:
        json.dump(fake_authors_json, file, default=str, indent=4)

    yield authros_file



def test_get_authors(client, temp_authors_db):
    response = client.get("/authors")
    assert response.status_code == 200
    items = response.json()['items']
    assert items[0]['author_id'] == 1
    assert items[1]['author_id'] == 2
    assert items[0]['name'] == 'Bitar'
    assert items[1]['name'] == 'Bakro'

def test_get_authors_does_not_return_creation_date(client, temp_authors_db):
    response = client.get("/authors")
    assert response.status_code == 200
    for author in response.json()['items']:
        assert "creation_date" not in author


def test_get_author_by_id(client, temp_authors_db):
    response = client.get("/authors/1")
    assert response.status_code == 200
    items = response.json()
    assert items['author_id'] == 1
    assert items['name'] == 'Bitar'

@pytest.mark.parametrize(
    "author_id, expected_status_code", 
    (
        (0, 422),
        (-1, 422),
        (-1000, 422),
        ("abc", 422),
        (100, 404),
    )
)
def test_get_author_by_id_not_found(client, temp_authors_db, author_id, expected_status_code):
    response = client.get(f"/authors/{author_id}", headers={"x-user-id" : "1"})
    assert response.status_code == expected_status_code

def test_create_author(client, temp_authors_db):
    new_author =     {    
        "name": "Ahmad",
        "birth_year": 20010,
        "added_at": 2020,
    }
    response = client.post("/authors", headers={'x-user-id':'123'}, json=new_author)
    assert response.status_code == 200
    assert response.json()['author_id'] == 3
    assert response.json()['name'] == new_author["name"]

def test_create_author_fails_with_invalid_data(client):
    invalid_author = {
        "title": "Invalid author",
        "author" : "Bitar",
        "genre" : "Sci-Fi"
    }
    response = client.post("/authors", headers={'x-user-id':'123'}, json=invalid_author)
    assert response.status_code == 422


def test_delete_author(client, temp_authors_db):
    response = client.delete("/authors/1", headers={'x-user-id':'123'})
    assert response.status_code == 200
    response = client.get("authors/1")
    assert response.status_code == 404

def test_delete_author_not_found(client, temp_authors_db):

        response = client.delete("/authors/4", headers={'x-user-id':'123'})
        assert response.status_code == 404
        assert response.json()['details'] == "Author with id 4 doesn't exist"

def test_update_author(client, temp_authors_db):
    updated_author = {    
        "name": "Muhammad Bitar",
        "birth_year": 2005
    }
    response = client.put("/authors/1", headers={'x-user-id':'123'}, json=updated_author)
    assert response.status_code == 200
    response = client.get("authors/1")
    assert response.status_code == 200
    updated_author_in_list = response.json()
    assert updated_author_in_list["name"] == updated_author["name"]
    assert updated_author_in_list["birth_year"] == updated_author["birth_year"]
