import asyncio
import os
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from main import app
from db.db_models.Base import Base

load_dotenv()
    

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://postgres:password@localhost:5432/library_test",
)


@pytest.fixture
def test_db(monkeypatch):
    test_engine = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
    test_sessionmaker = async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def init_models():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(init_models())

    monkeypatch.setattr("db.database.sessionmaker", test_sessionmaker)
    yield

    async def cleanup():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await test_engine.dispose()
    asyncio.run(cleanup())

@pytest.fixture
def client(test_db):
    return TestClient(app)

@pytest.fixture
def auth_headers(client):
    client.post("/auth/register", json={"name": "test", "email": "test@test.com", "password": "password123"})
    res = client.post("/auth/login", data={"username": "test@test.com", "password": "password123"})
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def create_author(client, auth_headers):
    response = client.post("/authors", json={"name": "test_author", "birth_year": 2000}, headers=auth_headers)
    return response.json()

@pytest.fixture
def create_book(client, auth_headers, create_author):
    response = client.post(
        "/books",
        json={
            "title": "test_book",
            "author_id": create_author["author_id"],
            "genre": "test_genre",
            "year": 2000,
        },
        headers=auth_headers,
    )
    return response.json()

@pytest.fixture
def create_user(client):
    response = client.post("/auth/register", json={"name": "user", "email": "user@example.com", "password": "password123"})
    return response.json()