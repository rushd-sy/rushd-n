import pytest
from datetime import datetime


def test_create_loan(client, auth_headers):
    response = client.post(
        "/loans",
        json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == 1
    assert data["user_id"] == 1
    assert datetime.fromisoformat(data["return_date"]) == datetime(2023, 1, 15)
    assert "loan_id" in data


@pytest.mark.parametrize(
    "invalid_input",
    [
        {"book_id": -1, "user_id": 1, "return_date": "2023-01-15"},
        {"book_id": 1, "user_id": -1, "return_date": "2023-01-15"},
        {"book_id": 1, "user_id": 1, "return_date": ""},
        {"book_id": 1, "user_id": 1},
        {"book_id": 1, "return_date": "2023-01-15"},
    ],
)
def test_create_loan_invalid_input(client, invalid_input, auth_headers):
    response = client.post("/loans", json=invalid_input, headers=auth_headers)
    assert response.status_code == 422


def test_update_loan_not_found(client, auth_headers):
    response = client.put(
        "/loans/999",
        json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"},
        headers=auth_headers,
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Loan not found"}


def test_unauthorized_access(client):
    response = client.post(
        "/loans", json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"}
    )
    assert response.status_code == 401

def test_delete_loan(client, auth_headers):
    response = client.post(
        "/loans",
        json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    loan_id = data["loan_id"]

    delete_response = client.delete(f"/loans/{loan_id}", headers=auth_headers)
    assert delete_response.status_code == 200
    deleted_data = delete_response.json()
    assert deleted_data["loan_id"] == loan_id

def test_get_loan(client, auth_headers):
    response = client.post(
        "/loans",
        json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    loan_id = data["loan_id"]

    get_response = client.get(f"/loans/{loan_id}", headers=auth_headers)
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["loan_id"] == loan_id

def test_auth_user_isnt_the_same_as_loan_user(client, auth_headers):
    response = client.post(
        "/loans",
        json={"book_id": 1, "user_id": 2, "return_date": "2026-08-30"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    loan_id = data["loan_id"]

    get_response = client.get(f"/loans/{loan_id}", headers=auth_headers)
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["user_id"] == 1