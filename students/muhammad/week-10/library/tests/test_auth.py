import pytest
import asyncio
from fastapi.testclient import TestClient
from freezegun import freeze_time
from sqlalchemy import select, func
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)

from main import app
from database.base import Base
from database.connection import get_db
from database.models.users import User
from config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture
def clear_db():
    engine = create_async_engine(
        TEST_DATABASE_URL,
        poolclass=NullPool
    )

    TestSession = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async def setup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(setup())

    yield TestSession

    async def teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()

    asyncio.run(teardown())


@pytest.fixture
def client(clear_db):
    TestSessionLocal = clear_db

    async def override_get_db():
        async with TestSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.pop(get_db, None)


def get_user_from_db(TestSession, username):
    async def query():
        async with TestSession() as db:
            user = await db.scalar(
                select(User).where(User.username == username)
            )

            if user is None:
                return None

            return {
                "user_id": user.user_id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "hashed_password": user.hashed_password
            }

    return asyncio.run(query())


def count_users(TestSession):
    async def query():
        async with TestSession() as db:
            return await db.scalar(
                select(func.count()).select_from(User)
            )

    return asyncio.run(query())


def test_registration_success(client, clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200

    db_user = get_user_from_db(clear_db, user["username"])

    assert count_users(clear_db) == 1
    assert db_user is not None
    assert db_user["username"] == user["username"]
    assert db_user["full_name"] == user["full_name"]
    assert db_user["email"] == user["email"]
    assert db_user["hashed_password"] != user["password"]

    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_registration_fails_with_invalid_username(client, clear_db):
    user = {
        "username": "Test User One",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert count_users(clear_db) == 0
    assert response.status_code == 422
    assert "username" in response.text.lower()


def test_registration_fails_with_invalid_email(client, clear_db):
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert count_users(clear_db) == 0
    assert response.status_code == 422
    assert "email" in response.text.lower()


def test_registration_fails_with_invalid_password(client, clear_db):
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "1234"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert count_users(clear_db) == 0
    assert response.status_code == 422
    assert "password" in response.text.lower()


def test_registration_fails_with_existing_email(client, clear_db):
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
        "/auth/register",
        json=user1
    )

    response2 = client.post(
        "/auth/register",
        json=user2
    )

    assert count_users(clear_db) == 1
    assert response1.status_code == 200
    assert response2.status_code == 409
    assert "email" in response2.text.lower()


def test_registration_fails_with_existing_username(client, clear_db):
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
        "/auth/register",
        json=user1
    )

    response2 = client.post(
        "/auth/register",
        json=user2
    )

    assert count_users(clear_db) == 1
    assert response1.status_code == 200
    assert response2.status_code == 409
    assert "username" in response2.text.lower()


def test_login_success(client, clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200
    assert count_users(clear_db) == 1

    user_login = {
        "username": "testuser1",
        "password": "password123"
    }

    response = client.post(
        "/auth/login",
        data=user_login
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_fails_with_wrong_password(client, clear_db):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200
    assert count_users(clear_db) == 1

    user_login = {
        "username": "testuser1",
        "password": "password"
    }

    response = client.post(
        "/auth/login",
        data=user_login
    )

    assert response.status_code == 401
    assert "invalid credentials" in response.text.lower()


def test_login_fails_with_not_existing_user(client):
    user_login = {
        "username": "testuser2",
        "password": "password123"
    }

    response = client.post(
        "/auth/login",
        data=user_login
    )

    assert response.status_code == 401
    assert "invalid credentials" in response.text.lower()


def test_login_fails_with_invalid_username(client):
    user = {
        "username": "testuser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200

    user_login = {
        "username": "test user",
        "password": "password123"
    }

    response = client.post(
        "/auth/login",
        data=user_login
    )

    assert response.status_code == 422
    assert "username" in response.text.lower()


def test_expired_jwt_fails(client):
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    token = response.json()["access_token"]

    get_response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert get_response.status_code == 200

    with freeze_time("2030-01-01"):
        get_response = client.get(
            "/books",
            headers={"Authorization": f"Bearer {token}"}
        )

        assert get_response.status_code == 401
        assert "session expired" in get_response.json()["detail"].lower()


def test_invalid_jwt_fails(client):
    user = {
        "username": "TestUser1",
        "full_name": "Test User",
        "email": "test1@example.com",
        "password": "password123"
    }

    response = client.post(
        "/auth/register",
        json=user
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json()["access_token"]
    invalid_token = token + "invalid"

    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {invalid_token}"}
    )

    assert response.status_code == 401
    assert "signature" in response.json()["detail"].lower()
