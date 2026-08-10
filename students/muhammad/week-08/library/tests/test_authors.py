from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)

fake_authors = [
    {    
        "author_id": 1,
        "name": "Bitar",
        "birth_year": 2005,
        "added_at": "2018",
    }, 
    {
        "author_id": 2,
        "name": "Bakro",
        "birth_year": 2005,
        "added_at": "2017",    
    }
]

fake_authors_response = [
    {    
        "author_id": 1,
        "name": "Bitar",
        "birth_year": 2005,
    }, 
    {
        "author_id": 2,
        "name": "Bakro",
        "birth_year": 2005,
    }
]

def test_get_authors():
    with patch("routers.authors.load_authors", return_value=fake_authors):
        response = client.get("/authors")
        assert response.status_code == 200
        assert response.json()['items'] == fake_authors_response

def test_get_authors_does_not_return_creation_date():
    with patch("routers.authors.load_authors", return_value=fake_authors):
        response = client.get("/authors")
        assert response.status_code == 200
        for author in response.json()['items']:
            assert "creation_date" not in author
        assert response.json()['items'] == fake_authors_response

def test_get_author_by_id():
    with patch("routers.authors.load_authors", return_value=fake_authors):
        response = client.get("/authors/1", headers={"x-user-id" : "1"})
        assert response.status_code == 200
        assert response.json() == fake_authors_response[0]

def test_get_author_by_id_not_found():
    with patch("routers.authors.load_authors", return_value=fake_authors):
        response = client.get("/authors/3", headers={"x-user-id" : "1"})
        assert response.status_code == 404
        assert response.json()['detail'] == "author with id 3 doesn't exist"

def test_create_author():
    new_author =     {    
        "name": "Ahmad",
        "birth_year": 20010,
        "added_at": 2020,
    }
    
    with patch(
        "routers.authors.load_authors", return_value=fake_authors
    ), patch(
        "routers.authors.save_authors"):

        response = client.post("/authors", json=new_author)
        assert response.status_code == 200
        assert response.json()['author_id'] == 3
        assert response.json()['name'] == new_author["name"]

def test_create_author_fails_with_invalid_data():
    invalid_author = {
        "title": "Invalid author",
        "author" : "Bitar",
        "genre" : "Sci-Fi"
    }
    response = client.post("/authors", json=invalid_author)
    assert response.status_code == 422


def test_delete_author():
    with patch(
        "routers.authors.load_authors",
        return_value=fake_authors.copy()
    ), patch(
        "routers.authors.save_authors"
    ) as mock_save_authors:

        response = client.delete("/authors/1")
        assert response.status_code == 200
        mock_save_authors.assert_called_once()
        saved_authors = mock_save_authors.call_args[0][0]
        assert all(author["author_id"] != 1 for author in saved_authors)
        
def test_delete_author_not_found():
    with patch(
        "routers.authors.load_authors",
        return_value=fake_authors.copy()
    ), patch(
        "routers.authors.save_authors"
    ) as mock_save_authors:

        response = client.delete("/authors/4")
        assert response.status_code == 404
        mock_save_authors.assert_not_called()
        assert response.json()['detail'] == "author with id 4 doesn't exist"

def test_update_author():
    updated_author = {    
        "name": "Muhammad Bitar",
        "birth_year": 2005
    }
    
    with patch(
        "routers.authors.load_authors",
        return_value=fake_authors.copy()
    ), patch(
        "routers.authors.save_authors"
    ) as mock_save_authors:

        response = client.put("/authors/1", json=updated_author)
        assert response.status_code == 200
        mock_save_authors.assert_called_once()
        saved_authors = mock_save_authors.call_args[0][0]
        updated_author_in_list = next((author for author in saved_authors if author["author_id"] == 1), None)
        assert updated_author_in_list is not None
        assert updated_author_in_list["name"] == updated_author["name"]
