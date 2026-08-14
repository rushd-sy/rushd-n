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
def temp_books_db(tmp_path, monkeypatch):
    books_file = tmp_path / "books_test.json"
    monkeypatch.setattr("utils.storage.BOOKS_FILE", books_file)
    
    fake_books_json = [
        {
            "book_id": 1,
            "title": "First Book",
            "author" : "Bitar",
            "genre" : "Horror",
            "publish_year": 2023,
            "creation_date": date(2020, 8, 30).isoformat()
        }, 
        {
            "book_id": 2,
            "title": "Second Book",
            "author" : "Bitar",
            "genre" : "Mystery",
            "publish_year": 1999,
            "creation_date": date(2020, 8, 30).isoformat()
        }
    ]
    with open(books_file, "w") as file:
        json.dump(fake_books_json, file, default=str, indent=4)

    yield books_file

def test_get_books(client, temp_books_db):
    response = client.get("/books")
    
    assert response.status_code == 200
    items = response.json()['items']
    assert items[0]['book_id'] == 1
    assert items[1]['book_id'] == 2
    assert items[0]['author'] == 'Bitar'
    assert items[1]['publish_year'] == 1999

def test_get_books_does_not_return_creation_date(client, temp_books_db):
    response = client.get("/books")
    assert response.status_code == 200
    for book in response.json()['items']:
        assert "creation_date" not in book
    assert response.json()['items'] 

def test_get_book_by_id(client, temp_books_db):
    response = client.get("/books/1")
    assert response.status_code == 200
    item = response.json()  
    assert item['book_id'] == 1
    assert item['title'] == 'First Book'
    assert item['genre'] == 'Horror'

@pytest.mark.parametrize(
    "book_id, expected_status_code",
    [
        (100, 404),
        (-1, 422),
        (-100, 422),
        ("abs", 422),
        ("az", 422)
    ]
)
def test_get_book_by_id_not_found(client, temp_books_db, book_id, expected_status_code):
    response = client.get(f"/books/{book_id}")
    assert response.status_code == expected_status_code

def test_create_book(client, temp_books_db):
    new_book = {
        "title": "Third Book",
        "author" : "Bitar",
        "genre" : "Sci-Fi",
        "publish_year": 2025
    }
    response = client.post("/books", headers={'x-user-id':'123'}, json=new_book)
    assert 1 == 1
    assert response.status_code == 200
    assert response.json()['book_id'] == 3
    assert response.json()['title'] == new_book['title']

def test_create_book_fails_with_invalid_data(client):
    invalid_book = {
        "title": "Invalid Book",
        "author" : "Bitar",
        "genre" : "Sci-Fi"
    }
    response = client.post("/books", headers={'x-user-id':'123'}, json=invalid_book)
    assert response.status_code == 422

def test_delete_book(client, temp_books_db):
    response = client.delete("/books/1", headers={"x-user-id":"123"})
    assert response.status_code == 200
    
    response = client.get("/books/1")
    assert response.status_code == 404

def test_delete_book_not_found(client, temp_books_db):
    response = client.delete("/books/4", headers={"x-user-id":"123"})
    assert response.status_code == 404
    assert response.json()['details'] == "Book with id 4 doesn't exist"

def test_update_book(client, temp_books_db):
    updated_book_request = {
        "title": "Updated Book",
        "author" : "Bitar",
        "genre" : "Sci-Fi",
        "publish_year": 2025
    }
    response = client.put("/books/1", headers={'x-user-id':'123'}, json=updated_book_request)
    assert response.status_code == 200
    
    updated_book_response = client.get("books/1").json()
    assert updated_book_request['title'] == updated_book_response['title']
    assert updated_book_request['author'] == updated_book_response['author']
    assert updated_book_request['genre'] == updated_book_response['genre']
    assert updated_book_request['publish_year'] == updated_book_response['publish_year']
