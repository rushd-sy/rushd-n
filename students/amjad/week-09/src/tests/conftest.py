import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def test_db(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "books.json").write_text("[]", encoding="utf-8")
    (tmp_path / "authors.json").write_text("[]", encoding="utf-8")
    (tmp_path / "loans.json").write_text("[]", encoding="utf-8")
    (tmp_path / "users.json").write_text("[]", encoding="utf-8")
    return tmp_path

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={"name": "test", "email": "test@test.com", "password": "password123"})
    res = client.post("/auth/login", data={"username": "test@test.com", "password": "password123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}