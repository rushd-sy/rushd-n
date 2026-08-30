from fastapi.testclient import TestClient
import pytest

from main import app
from utils.users_store import users
client = TestClient(app)

@pytest.fixture
def modify_expires_delta(monkeypatch):
    monkeypatch.setattr("config.settings.ACCESS_TOKEN_EXPIRE_MINUTES", 0)


@pytest.fixture
def clear_db():
    users.clear()
    return users

def test_registration_success(clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register/",
        json=user
    )
    
    assert response.status_code == 200
    assert len(users) == 1
    assert users[0].username == user["username"]
    assert users[0].full_name == user["full_name"]
    assert users[0].email == user["email"]
    assert users[0].password != user["password"]
    assert "access_token" in response.json()
    assert response.json()['token_type'] == 'bearer'

def test_registration_fails_with_invalid_username(clear_db):
    user = {
        "username": "Test Uesr One",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register",
        json=user
    )
    
    assert len(users) == 0
    assert response.status_code == 422
    assert "username" in response.text

def test_registration_fails_with_invalid_email(clear_db):
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register",
        json=user
    )
    
    assert len(users) == 0
    assert response.status_code == 422
    assert "email" in response.text.lower()

def test_registration_fails_with_invalid_password(clear_db):
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1example.com",
        "password": "1234"
    }
    
    response = client.post(
        "auth/register",
        json=user
    )
    
    assert len(users) == 0
    assert response.status_code == 422
    assert "password" in response.text.lower()

def test_registration_fails_with_existing_email(clear_db):
    user1 = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    user2 = {
        "username": "TestUser2",
        "full_name": "Test User 2",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response1 = client.post(
        "auth/register",
        json=user1
    )
    
    response2 = client.post(
        "auth/register",
        json=user2
    )
    
    assert len(users) == 1
    assert response1.status_code == 200
    assert response2.status_code == 409
    assert "email" in response2.text.lower()

def test_registration_fails_with_existing_username(clear_db):
    user1 = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    user2 = {
        "username": "TestUser1",
        "full_name": "Test User 2",
        "email": "test2@example.com",
        "password": "password123"
    }
    
    response1 = client.post(
        "auth/register",
        json=user1
    )
    
    response2 = client.post(
        "auth/register",
        json=user2
    )
    
    assert len(users) == 1
    assert response1.status_code == 200
    assert response2.status_code == 409
    assert "username" in response2.text.lower()

def test_login_success(clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register/",
        json=user
    )
    
    assert response.status_code == 200
    assert len(users) == 1

    user_login = {
        "username": "testuser1",
        "password": "password123"
    }

    response = client.post(
        "auth/login", 
        json=user_login
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()['token_type'] == 'bearer'

def test_login_fails_with_wrong_password(clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register/",
        json=user
    )
    
    assert response.status_code == 200
    assert len(users) == 1

    user_login = {
        "username": "testuser1",
        "password": "password"
    }

    response = client.post(
        "auth/login", 
        json=user_login
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.text.lower()

def test_login_fails_with_not_existing_user(clear_db):
    user_login = {
        "username": "testuser2",
        "password": "password123"
    }

    response = client.post(
        "auth/login", 
        json=user_login
    )
    
    assert response.status_code == 401
    assert "invalid credentials" in response.text.lower()

def test_login_fails_with_invalid_username(clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register/",
        json=user
    )
    
    assert response.status_code == 200
    assert len(users) == 1

    user_login = {
        "username": "test user",
        "password": "password123"
    }

    response = client.post(
        "auth/login", 
        json=user_login
    )
    
    assert response.status_code == 422
    assert "username" in response.text.lower()

def test_expired_jwt_fails(clear_db, modify_expires_delta):
    # assert int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")) == 0 # type: ignore
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }
    
    response = client.post(
        "auth/register",
        json=user
    )
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()['token_type'] == "bearer"
    
    print(response.json()['access_token'])
    get_resopnse = client.get(
        "/books",
        headers={"Authorization": f"Bearer {response.json()['access_token']}"}
    )
    
    assert get_resopnse.status_code == 401
    assert "session expired" in get_resopnse.json()['detail'].lower()
