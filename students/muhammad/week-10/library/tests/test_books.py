from datetime import date
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
from database.models.books import Book

from config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture
def temp_books_db():
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
            author = Author(
                name="Bitar",
                birth_year=2005
            )

            db.add(author)
            await db.flush()

            books = [
                Book(
                    title="First Book",
                    author_id=author.author_id,
                    genre="Horror",
                    publish_year=2023
                ),
                Book(
                    title="Second Book",
                    author_id=author.author_id,
                    genre="Mystery",
                    publish_year=1999
                )
            ]

            db.add_all(books)
            await db.commit()

            return {
                "author_id": author.author_id,
                "book_ids": [
                    books[0].book_id,
                    books[1].book_id
                ]
            }

    database_data = asyncio.run(setup())

    yield {
        "engine": engine,
        "session": TestSession,
        "author_id": database_data["author_id"],
        "book_ids": database_data["book_ids"]
    }

    async def teardown():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()

    asyncio.run(teardown())


@pytest.fixture
def client(temp_books_db):
    TestSessionLocal = temp_books_db["session"]

    async def override_get_db():
        async with TestSessionLocal() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.pop(get_db, None)


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


def test_get_books(client, access_token, temp_books_db):
    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    items = response.json()["items"]
    book_ids = temp_books_db["book_ids"]
    author_id = temp_books_db["author_id"]

    assert items[0]["book_id"] == book_ids[0]
    assert items[1]["book_id"] == book_ids[1]

    assert items[0]["author_id"] == author_id
    assert items[1]["author_id"] == author_id

    assert items[0]["title"] == "First Book"
    assert items[1]["publish_year"] == 1999


def test_get_books_does_not_return_creation_date(client, access_token):
    response = client.get(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    for book in response.json()["items"]:
        assert "creation_date" not in book

    assert response.json()["items"]


def test_get_book_by_id(client, access_token, temp_books_db):
    book_id = temp_books_db["book_ids"][0]

    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    item = response.json()

    assert item["book_id"] == book_id
    assert item["title"] == "First Book"
    assert item["genre"] == "Horror"


@pytest.mark.parametrize(
    "book_id, expected_status_code",
    [
        (100, 404),
        (-1, 422),
        (-100, 422),
        ("abs", 422),
        ("az", 422)
    ]
)
def test_get_book_by_id_not_found(
    client, access_token, book_id, expected_status_code
):
    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == expected_status_code


def test_create_book(client, access_token, temp_books_db):
    new_book = {
        "title": "Third Book",
        "author_id": temp_books_db["author_id"],
        "genre": "Sci-Fi",
        "publish_year": 2025
    }

    response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_book
    )

    assert response.status_code == 200
    assert response.json()["title"] == new_book["title"]
    assert response.json()["author_id"] == new_book["author_id"]
    assert response.json()["book_id"] is not None


def test_create_book_fails_with_invalid_data(client, access_token):
    invalid_book = {
        "title": "Invalid Book",
        "genre": "Sci-Fi"
    }

    response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"},
        json=invalid_book
    )

    assert response.status_code == 422


def test_delete_book(client, access_token, temp_books_db):
    book_id = temp_books_db["book_ids"][0]

    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404


def test_delete_book_not_found(client, access_token):
    response = client.delete(
        "/books/100",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json()["details"] == "Book with id 100 doesn't exist"


def test_update_book(client, access_token, temp_books_db):
    book_id = temp_books_db["book_ids"][0]

    updated_book_request = {
        "title": "Updated Book",
        "author_id": temp_books_db["author_id"],
        "genre": "Sci-Fi",
        "publish_year": 2025
    }

    response = client.put(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_book_request
    )

    assert response.status_code == 200

    updated_book_response = client.get(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    ).json()

    assert updated_book_request["title"] == updated_book_response["title"]
    assert updated_book_request["author_id"] == updated_book_response["author_id"]
    assert updated_book_request["genre"] == updated_book_response["genre"]
    assert updated_book_request["publish_year"] == updated_book_response["publish_year"]



def test_get_books_with_filters(client, access_token, temp_books_db):
    author_id = temp_books_db["author_id"]

    old_book = {
        "title": "Old Horror",
        "author_id": author_id,
        "genre": "Horror",
        "publish_year": 1998
    }

    create_response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"},
        json=old_book
    )

    assert create_response.status_code == 200

    response = client.get(
        "/books",
        params={
            "author_id": author_id,
            "genre": "Horror",
            "min_publish_year": 2000
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    items = response.json()["items"]

    assert len(items) == 1
    assert items[0]["title"] == "First Book"
    

def test_get_books_with_pagination(client, access_token):
    response = client.get(
        "/books",
        params={"offset": 1, "limit": 1},
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Second Book"

def test_create_book_with_non_existing_author(client, access_token):
    new_book = {
        "title": "Unknown Author Book",
        "author_id": 999999,
        "genre": "Fantasy",
        "publish_year": 2025
    }

    response = client.post(
        "/books",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_book
    )

    assert response.status_code == 404
    

def test_update_book_with_non_existing_author(
    client, access_token, temp_books_db
):
    book_id = temp_books_db["book_ids"][0]

    updated_book = {
        "title": "Updated Book",
        "author_id": 999999,
        "genre": "Fantasy",
        "publish_year": 2025
    }

    response = client.put(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_book
    )

    assert response.status_code == 404
    


def test_update_book_not_found(client, access_token, temp_books_db):
    updated_book = {
        "title": "Updated Book",
        "author_id": temp_books_db["author_id"],
        "genre": "Fantasy",
        "publish_year": 2025
    }

    response = client.put(
        "/books/100",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_book
    )

    assert response.status_code == 404


def test_delete_book_with_loans(
    client, access_token, temp_books_db
):
    book_id = temp_books_db["book_ids"][0]

    loan = {
        "book_id": book_id,
        "loan_date": date.today().isoformat()
    }

    loan_response = client.post(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        json=loan
    )

    assert loan_response.status_code == 200

    response = client.delete(
        f"/books/{book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 409
