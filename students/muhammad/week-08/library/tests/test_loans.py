import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

from main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def fake_loans():
    fake_loans_json = [
    {
        "loan_id": 1,
        "book_id": 2,
        "date": "2025-01-04T00:00:00",
        "name" : "Amjad",
        "added_at": "2025-01-03T00:00:00"
    }, 
    {
        "loan_id": 2,
        "book_id": 1,
        "date": "2025-01-03T00:00:00",
        "name" : "Muhammad",
        "added_at": "2025-01-01T00:00:00"
    }
]
    return fake_loans_json.copy()

@pytest.fixture
def fake_loans_response():
    fake_loans_response_json = [
    {
        "loan_id": 1,
        "book_id": 2,
        "date": "2025-01-04T00:00:00",
        "name" : "Amjad",
    }, 
    {
        "loan_id": 2,
        "book_id": 1,
        "date": "2025-01-03T00:00:00",
        "name" : "Muhammad",
    }
    ]    
    return fake_loans_response_json.copy()

def test_get_loans(client, fake_loans, fake_loans_response):
    with patch("routers.loans.load_loans", return_value=fake_loans):
        response = client.get("/loans")
        assert response.status_code == 200
        assert response.json()['items'] == fake_loans_response

def test_get_loans_does_not_return_creation_date(client, fake_loans, fake_loans_response):
    with patch("routers.loans.load_loans", return_value=fake_loans):
        response = client.get("/loans")
        assert response.status_code == 200
        for loan in response.json()['items']:
            assert "creation_date" not in loan
        assert response.json()['items'] == fake_loans_response

def test_get_loan_by_id(client, fake_loans, fake_loans_response):
    with patch("routers.loans.load_loans", return_value=fake_loans):
        response = client.get("/loans/1", headers={"x-user-id" : "1"})
        assert response.status_code == 200
        assert response.json() == fake_loans_response[0]

@pytest.mark.parametrize(
    "loan_id, expected_statur_code",
    (
        (0, 422),
        (-1, 422),
        (-1000, 422),
        ("abc", 422),
        (100, 404),
    )
)
def test_get_loan_by_id_not_found(client, fake_loans, loan_id, expected_statur_code):
    with patch("routers.loans.load_loans", return_value=fake_loans):
        response = client.get(f"/loans/{loan_id}", headers={"x-user-id" : "1"})
        assert response.status_code == expected_statur_code

def test_create_loan(client, fake_loans):
    new_loan = {
        "book_id": 2,
        "date": "2025-01-04T00:00:00",
        "name" : "Bitar",
        "added_at": "2025-01-07T00:00:00"
    }
    
    with patch(
        "routers.loans.load_loans", return_value=fake_loans
    ), patch(
        "routers.loans.save_loans"):

        response = client.post("/loans", json=new_loan)
        assert response.status_code == 200
        assert response.json()['loan_id'] == 3
        assert response.json()['book_id'] == new_loan["book_id"]

def test_create_loan_fails_with_invalid_data(client):
    invalid_loan = {
        "title": "Invalid loan",
        "author" : "Bitar",
        "genre" : "Sci-Fi"
    }
    response = client.post("/loans", json=invalid_loan)
    assert response.status_code == 422


def test_delete_loan(client, fake_loans):
    with patch(
        "routers.loans.load_loans",
        return_value=fake_loans.copy()
    ), patch(
        "routers.loans.save_loans"
    ) as mock_save_loans:

        response = client.delete("/loans/1")
        assert response.status_code == 200
        mock_save_loans.assert_called_once()
        saved_loans = mock_save_loans.call_args[0][0]
        assert all(loan["loan_id"] != 1 for loan in saved_loans)
        
def test_delete_loan_not_found(client, fake_loans):
    with patch(
        "routers.loans.load_loans",
        return_value=fake_loans.copy()
    ), patch(
        "routers.loans.save_loans"
    ) as mock_save_loans:

        response = client.delete("/loans/4")
        assert response.status_code == 404
        mock_save_loans.assert_not_called()
        assert response.json()['detail'] == "loan with id 4 doesn't exist"

def test_update_loan(client, fake_loans):
    updated_loan =     {
        "book_id": 5,
        "date": "2025-01-010T00:00:00",
        "name" : "Amjad",
    }
    with patch(
        "routers.loans.load_loans",
        return_value=fake_loans.copy()
    ), patch(
        "routers.loans.save_loans"
    ) as mock_save_loans:

        response = client.put("/loans/1", json=updated_loan)
        assert response.status_code == 200
        mock_save_loans.assert_called_once()
        saved_loans = mock_save_loans.call_args[0][0]
        updated_loan_in_list = next((loan for loan in saved_loans if loan["loan_id"] == 1), None)
        assert updated_loan_in_list is not None
        assert updated_loan_in_list["book_id"] == updated_loan["book_id"]
