
import datetime
import json


def test_register_user(client):
    response = client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    with open("users.json", "r", encoding="utf-8") as f:
        users = json.loads(f.read())
    assert response.status_code == 200
    assert any(user['email'] == 'testuser@gmail.com' for user in users)
    assert any(user['password'] != 'testpassword' for user in users)
    assert any(user['name'] == 'Test' for user in users)

def test_login_user(client):
    client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json()

def test_email_already_registered(client):
    client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    response = client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_login_invalid_password(client):
    client.post('/auth/register', json={
            'name': 'Test',
            'email': 'testuser@gmail.com',
            'password': 'testpassword'
        })
    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': 'invalidpassword'
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "email or password is incorrect"}

def test_login_nonexistent_user(client):
    response = client.post('/auth/login', data={
        'username': 'nonexistentuser@gmail.com',
        'password': 'testpassword'
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "email or password is incorrect"}

def test_delete_user(client):
    client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    token = response.json()['access_token']
    response = client.delete('auth/users/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

def test_valid_token_deleted_user(client):
    client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    token = response.json()['access_token']
    response = client.delete('auth/users/1', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    response = client.post('/loans/', headers={'Authorization': f'Bearer {token}'}, json={
        'book_id': 1,
        'user_id': 1,
        'return_date': '2026-08-30'
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_expired_token(client, monkeypatch):
    class FakeDatetime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.datetime.now(tz) - datetime.timedelta(minutes=31)
        
    monkeypatch.setattr("services.auth_service.datetime", FakeDatetime)
    client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    token = response.json()['access_token']
    response = client.post('/loans/', headers={'Authorization': f'Bearer {token}'}, json={
        'book_id': 1,
        'user_id': 1,
        'return_date': '2026-08-30'
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Token has expired"}

def test_invalid_token(client):
    response = client.post('/loans/', headers={'Authorization': 'Bearer invalidtoken'}, json={
        'book_id': 1,
        'user_id': 1
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}

def test_token_signed_with_wrong_secret(client, monkeypatch):
    monkeypatch.setattr("services.auth_service.SECRET_KEY", "wrongsecret")
    client.post('/auth/register', json={
        'name': 'Test',
        'email': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    response = client.post('/auth/login', data={
        'username': 'testuser@gmail.com',
        'password': 'testpassword'
    })
    token = response.json()['access_token']
    response = client.post('/loans/', headers={'Authorization': f'Bearer {token}'}, json={
        'book_id': 1,
        'user_id': 1,
        'return_date': '2026-08-30'
    })
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid token"}