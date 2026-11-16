import pytest
from fastapi.testclient import TestClient
import asyncio
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)


from main import app
from database.base import Base
from database.connection import get_db
from database.models.authors import Author
from config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

@pytest.fixture
def temp_authors_db():
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

        async with TestSession() as db:
            authors = [
                Author(name="Bitar", birth_year=2005),
                Author(name="Bakro", birth_year=2005)
            ]

            db.add_all(authors)
            await db.commit()

            return [
                authors[0].author_id,
                authors[1].author_id
            ]

    author_ids = asyncio.run(setup())

    yield {
        "engine": engine,
        "session": TestSession,
        "author_ids": author_ids
    }

    async def teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()

    asyncio.run(teardown())


@pytest.fixture
def client(temp_authors_db):
    TestSessionLocal = temp_authors_db["session"]

    async def override_get_db():
        async with TestSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture
def register_user(client):
    user = {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }

    response = client.post("/auth/register", json=user)

    assert response.status_code == 200, response.text

    yield response.json()


@pytest.fixture
def access_token(register_user):
    yield register_user["access_token"]


def test_get_authors(client, access_token, temp_authors_db):
    response = client.get(
        "/authors",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    items = response.json()["items"]
    author_ids = temp_authors_db["author_ids"]

    assert items[0]["author_id"] == author_ids[0]
    assert items[1]["author_id"] == author_ids[1]
    assert items[0]["name"] == "Bitar"
    assert items[1]["name"] == "Bakro"


def test_get_authors_does_not_return_creation_date(client, access_token):
    response = client.get(
        "/authors",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    for author in response.json()["items"]:
        assert "creation_date" not in author


def test_get_author_by_id(client, access_token, temp_authors_db):
    author_id = temp_authors_db["author_ids"][0]

    response = client.get(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    items = response.json()

    assert items["author_id"] == author_id
    assert items["name"] == "Bitar"


@pytest.mark.parametrize(
    "author_id, expected_status_code",
    (
        (0, 422),
        (-1, 422),
        (-1000, 422),
        ("abc", 422),
        (100, 404),
    )
)
def test_get_author_by_id_not_found(
    client, access_token, author_id, expected_status_code
):
    response = client.get(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == expected_status_code


def test_create_author(client, access_token):
    new_author = {
        "name": "Ahmad",
        "birth_year": 2010
    }

    response = client.post(
        "/authors",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_author
    )

    assert response.status_code == 200
    assert response.json()["name"] == new_author["name"]
    assert response.json()["author_id"] is not None


def test_create_author_fails_with_invalid_data(client, access_token):
    invalid_author = {
        "title": "Invalid author",
        "author": "Bitar",
        "genre": "Sci-Fi"
    }

    response = client.post(
        "/authors",
        headers={"Authorization": f"Bearer {access_token}"},
        json=invalid_author
    )

    assert response.status_code == 422


def test_delete_author(client, access_token, temp_authors_db):
    author_id = temp_authors_db["author_ids"][0]

    response = client.delete(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    response = client.get(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404


def test_delete_author_not_found(client, access_token):
    response = client.delete(
        "/authors/100",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json()["details"] == "Author with id 100 doesn't exist"


def test_update_author(client, access_token, temp_authors_db):
    author_id = temp_authors_db["author_ids"][0]

    updated_author = {
        "name": "Muhammad Bitar",
        "birth_year": 2005
    }

    response = client.put(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_author
    )

    assert response.status_code == 200

    response = client.get(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    updated_author_in_list = response.json()

    assert updated_author_in_list["name"] == updated_author["name"]
    assert updated_author_in_list["birth_year"] == updated_author["birth_year"]

def test_get_authors_with_name_filter(client, access_token):
    response = client.get(
        "/authors",
        params={"name": "Bitar"},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    items = response.json()["items"]

    assert len(items) == 1
    assert items[0]["name"] == "Bitar"

def test_get_authors_with_birth_year_range(client, access_token):
    response = client.get(
        "/authors",
        params={
            "min_birth_year": 2005,
            "max_birth_year": 2005
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    items = response.json()["items"]

    assert len(items) == 2
    assert items[0]["name"] == "Bitar"

def test_get_authors_with_pagination(client, access_token):
    response = client.get(
        "/authors",
        params={"offset": 1, "limit": 1},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Bakro"

def test_update_author_not_found(client, access_token):
    updated_author = {
        "name": "blablabl",
        "birth_year": 2000
    }

    response = client.put(
        "/authors/100",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_author
    )

    assert response.status_code == 404

def test_delete_author_with_books(client, access_token, temp_authors_db):
    author_id = temp_authors_db["author_ids"][0]

    book = {
        "title": "Author's Book",
        "author_id": author_id,
        "genre": "Fantasy",
        "publish_year": 2020
    }

    create_response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"},
        json=book
    )

    assert create_response.status_code == 200

    response = client.delete(
        f"/authors/{author_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 409

def test_wrong_parameters_fail(client, access_token, temp_authors_db):
    response = client.get(
        "/authors",
        params={"offset": -1, "limit": 1},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
    
    response = client.get(
        "/authors",
        params={"offset": 0, "limit": 100},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400

    response = client.get(
        "/authors",
        params={"offset": 0, "limit": 200},
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 400
