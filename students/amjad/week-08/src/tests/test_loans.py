import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    db_file = tmp_path / "loans.json"
    db_file.write_text("[]", encoding="utf-8")

    return db_file


@pytest.fixture
def client(test_db):
    return TestClient(app)


def test_create_loan(client):
    # fix the return date bug cause it now uses datetime datatype instead of string
    response = client.post(
        "/loans",
        json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"},
        headers={"X-User-Id": "1"},
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
def test_create_loan_invalid_input(client, invalid_input):
    response = client.post("/loans", json=invalid_input)
    assert response.status_code == 422


def test_update_loan_not_found(client):
    response = client.put(
        "/loans/999",
        json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"},
        headers={"X-User-Id": "1"},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Loan not found"}


def test_unauthorized_access(client):
    response = client.post(
        "/loans", json={"book_id": 1, "user_id": 1, "return_date": "2023-01-15"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "unauthorized"}
