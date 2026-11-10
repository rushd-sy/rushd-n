import asyncio
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from main import app
from db.database import get_db
from db.db_models import Base

@pytest.fixture
def test_db(tmp_path):
    test_db_path = tmp_path / "test.db"
    test_db_url = f"sqlite+aiosqlite:///{test_db_path}"

    test_engine = create_async_engine(test_db_url)
    test_sessionmaker = async_sessionmaker(
        bind=test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def init_models():
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    asyncio.run(init_models())

    async def override_get_db():
        async with test_sessionmaker() as session:
            try:
                yield session
            finally:
                await session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield

    app.dependency_overrides.clear()
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