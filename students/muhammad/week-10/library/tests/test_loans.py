import pytest
from fastapi.testclient import TestClient
from datetime import date
import json 

from main import app
from utils.users_store import users

@pytest.fixture
def temp_loans_db(tmp_path, monkeypatch):
    loans_file = tmp_path / "loans_test.json"
    monkeypatch.setattr("utils.storage.LOANS_FILE", loans_file)
    fake_loans_json = [
        {
            "loan_id": 1,
            "book_id": 2,
            "loan_date": date.today().isoformat(),
            "name" : "Amjad",
            "added_at": date.today().isoformat()
        }, 
        {
            "loan_id": 2,
            "book_id": 1,
            "loan_date": date.today().isoformat(),
            "name" : "Muhammad",
            "added_at": date.today().isoformat()
        },
        {
            "loan_id": 3,
            "book_id": 101,
            "loan_date": "2026-01-20",
            "name": "Alice Johnson",
            "added_at": "2026-01-20"
        },
        {
            "loan_id": 4,
            "book_id": 102,
            "loan_date": "2026-01-20",
            "name": "Alice Johnson",
            "added_at": "2026-01-20"
        },
    ]
    
    with open(loans_file, 'w') as file:
        json.dump(fake_loans_json, file, default=str, indent=4)
    
    yield loans_file

@pytest.fixture
def client(temp_loans_db):
    with TestClient(app) as c:
        yield c

@pytest.fixture
def register_user():
    with TestClient(app) as client:
        user = {
            "user_id": 1,
            "username": "testuser",
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        users.clear()
        yield client.post("/auth/register", json=user).json()


@pytest.fixture
def access_token(register_user):
    return register_user['access_token']

def test_get_loans(client, access_token):
    response = client.get(
        "/loans",
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    items = response.json()['items']
    assert items[0]['loan_id'] == 1
    assert items[1]['loan_id'] == 2
    assert items[0]['book_id'] == 2
    assert items[1]['book_id'] == 1
    assert items[0]['loan_date'] == date.today().isoformat()
    assert items[1]['loan_date'] == date.today().isoformat()

def test_get_loans_filterd(client, access_token):
    response = client.get(
        '/loans', 
        params={"loan_date":"2026-01-20"},
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200

    items = response.json()['items']
    assert len(items) == 2
    assert items[0]['loan_id'] == 3
    assert items[1]['loan_id'] == 4
    assert items[0]['book_id'] == 101
    assert items[1]['book_id'] == 102
    assert items[0]['loan_date'] == "2026-01-20"
    assert items[1]['loan_date'] == "2026-01-20"



def test_get_loans_does_not_return_creation_date(client, access_token):
    response = client.get(
        "/loans",
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    for loan in response.json()['items']:
        assert "creation_date" not in loan

def test_get_loan_by_id(client, access_token):
    response = client.get(
        "/loans/1",
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    item = response.json()
    assert item['loan_id'] == 1
    assert item['book_id'] == 2
    assert item['name'] == 'Amjad'

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
def test_get_loan_by_id_not_found(client, access_token, loan_id, expected_statur_code):
    response = client.get(
        f"/loans/{loan_id}",
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == expected_statur_code

def test_create_loan(client, access_token):
    new_loan = {
        "book_id": 2,
        "loan_date": date.today().isoformat(),
        "name" : "Bitar",
    }

    response = client.post("/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_loan
    )
    assert response.status_code == 200
    assert response.json()['loan_id'] == 5
    assert response.json()['book_id'] == new_loan["book_id"]

def test_create_loan_fails_with_invalid_data(client, access_token):
    invalid_loan = {
        "title": "Invalid loan",
        "author" : "Bitar",
        "genre" : "Sci-Fi"
    }
    response = client.post("/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        json=invalid_loan
    )
    assert response.status_code == 422


def test_delete_loan(client, access_token):
    response = client.delete(
        "/loans/1",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 200
    response = client.get(
        "/loans/1",
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 404        

def test_delete_loan_not_found(client, access_token):
    response = client.delete(
        "/loans/200",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404
    assert response.json()['details'] == "Loan with id 200 doesn't exist"

def test_update_loan(client, access_token):
    updated_loan =     {
        "book_id": 5,
        "loan_date": date.today().isoformat(),
        "name" : "Amjad",
    }

    response = client.put(
        "/loans/1",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_loan
    )
    assert response.status_code == 200
    response = client.get(
        '/loans/1',
        headers= {"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    item = response.json()
    assert item['book_id'] == 5 
    assert item['loan_date'] == date.today().isoformat()
    assert item['name'] == 'Amjad' 
