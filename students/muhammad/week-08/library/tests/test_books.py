from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

client = TestClient(app)

fake_books = [
    {
        "book_id": 1,
        "title": "First Book",
        "author" : "Bitar",
        "genre" : "Horror",
        "publish_year": 2023,
        "creation_date": "2025-01-01T00:00:00"
    }, 
    {
        "book_id": 2,
        "title": "Second Book",
        "author" : "Bitar",
        "genre" : "Mystery",
        "publish_year": 1999,
        "creation_date": "2025-01-01T00:00:00"
    }
]

fake_books_response = [
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

def test_get_books():
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books")
        assert response.status_code == 200
        assert response.json()['items'] == fake_books_response

def test_get_books_does_not_return_creation_date():
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books")
        assert response.status_code == 200
        for book in response.json()['items']:
            assert "creation_date" not in book
        assert response.json()['items'] == fake_books_response

def test_get_book_by_id():
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books/1", headers={"x-user-id" : "1"})
        assert response.status_code == 200
        assert response.json() == fake_books_response[0]

def test_get_book_by_id_not_found():
    with patch("services.book_services.load_books", return_value=fake_books):
        response = client.get("/books/3", headers={"x-user-id" : "1"})
        assert response.status_code == 404
        assert response.json()['details'] == "Book with id 3 doesn't exist"

def test_create_book():
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
        assert response.status_code == 200
        assert response.json()['book_id'] == 3
        assert response.json()['title'] == new_book['title']

def test_create_book_fails_with_invalid_data():
    invalid_book = {
        "title": "Invalid Book",
        "author" : "Bitar",
        "genre" : "Sci-Fi"
    }
    response = client.post("/books", json=invalid_book)
    assert response.status_code == 422


def test_delete_book():
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
        
def test_delete_book_not_found():
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

def test_update_book():
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
