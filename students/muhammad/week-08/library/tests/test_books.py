import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from datetime import date

from main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def fake_books():
    fake_books_json = [
        {
            "book_id": 1,
            "title": "First Book",
            "author" : "Bitar",
            "genre" : "Horror",
            "publish_year": 2023,
            "creation_date": date(2020, 8, 30) 
        }, 
        {
            "book_id": 2,
            "title": "Second Book",
            "author" : "Bitar",
            "genre" : "Mystery",
            "publish_year": 1999,
            "creation_date": date(2020, 8, 30) 
        }
    ]
    return fake_books_json.copy()

@pytest.fixture
def fake_books_response():
    fake_books_response_json = [
        {
            "book_id": 1,
            "title": "First Book",
            "author" : "Bitar",
            "genre" : "Horror",
            "publish_year": 2023
        }, 
        {
            "book_id": 2,
            "title": "Second Book",
            "author" : "Bitar",
            "genre" : "Mystery",
            "publish_year": 1999
        }
    ]
    return fake_books_response_json.copy()

def test_get_books(client, fake_books, fake_books_response):
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json()['items'] == fake_books_response

def test_get_books_does_not_return_creation_date(client, fake_books, fake_books_response):
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books")
        assert response.status_code == 200
        for book in response.json()['items']:
            assert "creation_date" not in book
        assert response.json()['items'] == fake_books_response

def test_get_book_by_id(client, fake_books, fake_books_response):
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books/1", headers={"x-user-id" : "1"})
        assert response.status_code == 200
        assert response.json() == fake_books_response[0]

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
def test_get_book_by_id_not_found(client, fake_books, book_id, expected_status_code):
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get(f"/books/{book_id}", headers={"x-user-id" : "1"})
        assert response.status_code == expected_status_code

def test_create_book(client, fake_books):
    new_book = {
        "title": "Third Book",
        "author" : "Bitar",
        "genre" : "Sci-Fi",
        "publish_year": 2025
    }
    with patch(
        "services.book_services.load_books", return_value=fake_books
    ), patch(
        "services.book_services.save_books"):

        response = client.post("/books", json=new_book)
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
    response = client.post("/books", json=invalid_book)
    assert response.status_code == 422


def test_delete_book(client, fake_books):
    with patch(
        "services.book_services.load_books",
        return_value=fake_books.copy()
    ), patch(
        "services.book_services.save_books"
    ) as mock_save_books:

        response = client.delete("/books/1")
        assert response.status_code == 200
        mock_save_books.assert_called_once()
        saved_books = mock_save_books.call_args[0][0]
        assert all(book["book_id"] != 1 for book in saved_books)
        
def test_delete_book_not_found(client, fake_books):
    with patch(
        "services.book_services.load_books",
        return_value=fake_books.copy()
    ), patch(
        "services.book_services.save_books"
    ) as mock_save_books:

        response = client.delete("/books/4")
        assert response.status_code == 404
        mock_save_books.assert_not_called()
        assert response.json()['details'] == "Book with id 4 doesn't exist"

def test_update_book(client, fake_books):
    updated_book = {
        "title": "Updated Book",
        "author" : "Bitar",
        "genre" : "Sci-Fi",
        "publish_year": 2025
    }
    with patch(
        "services.book_services.load_books",
        return_value=fake_books.copy()
    ), patch(
        "services.book_services.save_books"
    ) as mock_save_books:

        response = client.put("/books/1", json=updated_book)
        assert response.status_code == 200
        mock_save_books.assert_called_once()
        saved_books = mock_save_books.call_args[0][0]
        updated_book_in_list = next((book for book in saved_books if book["book_id"] == 1), None)
        assert updated_book_in_list is not None
        assert updated_book_in_list["title"] == updated_book["title"]
