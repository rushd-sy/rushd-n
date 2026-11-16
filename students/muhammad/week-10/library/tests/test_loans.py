import pytest
from fastapi.testclient import TestClient
from datetime import date
import asyncio
from sqlalchemy import select
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
from database.models.loans import Loan
from database.models.users import User
from config import settings


TEST_DATABASE_URL = settings.TEST_DATABASE_URL


@pytest.fixture
def temp_loans_db():
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
                ),
                Book(
                    title="Third Book",
                    author_id=author.author_id,
                    genre="Fantasy",
                    publish_year=2020
                ),
                Book(
                    title="Fourth Book",
                    author_id=author.author_id,
                    genre="Drama",
                    publish_year=2021
                ),
                Book(
                    title="Fifth Book",
                    author_id=author.author_id,
                    genre="Sci-Fi",
                    publish_year=2025
                )
            ]

            db.add_all(books)
            await db.commit()

            return {
                "author_id": author.author_id,
                "book_ids": [
                    book.book_id for book in books
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
def client(temp_loans_db):
    TestSessionLocal = temp_loans_db["session"]

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


@pytest.fixture
def temp_loans(register_user, temp_loans_db):
    TestSession = temp_loans_db["session"]
    book_ids = temp_loans_db["book_ids"]

    async def setup():
        async with TestSession() as db:
            user = await db.scalar(
                select(User).where(User.username == "testuser")
            )

            loans = [
                Loan(
                    book_id=book_ids[1],
                    user_id=user.user_id,
                    loan_date=date.today()
                ),
                Loan(
                    book_id=book_ids[0],
                    user_id=user.user_id,
                    loan_date=date.today()
                ),
                Loan(
                    book_id=book_ids[2],
                    user_id=user.user_id,
                    loan_date=date(2026, 1, 20)
                ),
                Loan(
                    book_id=book_ids[3],
                    user_id=user.user_id,
                    loan_date=date(2026, 1, 20)
                )
            ]

            db.add_all(loans)
            await db.commit()

            return {
                "user_id": user.user_id,
                "loan_ids": [
                    loan.loan_id for loan in loans
                ]
            }

    loan_data = asyncio.run(setup())

    return loan_data


def test_get_loans(client, access_token, temp_loans, temp_loans_db):
    response = client.get(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    items = response.json()["items"]

    items.sort(key=lambda item: item["loan_id"])

    loan_ids = temp_loans["loan_ids"]
    book_ids = temp_loans_db["book_ids"]

    assert items[0]["loan_id"] == loan_ids[0]
    assert items[1]["loan_id"] == loan_ids[1]

    assert items[0]["book_id"] == book_ids[1]
    assert items[1]["book_id"] == book_ids[0]

    assert items[0]["loan_date"] == date.today().isoformat()
    assert items[1]["loan_date"] == date.today().isoformat()


def test_get_loans_filtered(client, access_token, temp_loans, temp_loans_db):
    response = client.get(
        "/loans",
        params={
            "min_date": "2026-01-20",
            "max_date": "2026-01-20"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    items = response.json()["items"]
    items.sort(key=lambda item: item["loan_id"])

    loan_ids = temp_loans["loan_ids"]
    book_ids = temp_loans_db["book_ids"]

    assert len(items) == 2

    assert items[0]["loan_id"] == loan_ids[2]
    assert items[1]["loan_id"] == loan_ids[3]

    assert items[0]["book_id"] == book_ids[2]
    assert items[1]["book_id"] == book_ids[3]

    assert items[0]["loan_date"] == "2026-01-20"
    assert items[1]["loan_date"] == "2026-01-20"


def test_get_loans_does_not_return_creation_date(
    client, access_token, temp_loans
):
    response = client.get(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    for loan in response.json()["items"]:
        assert "creation_date" not in loan

    assert response.json()["items"]


def test_get_loan_by_id(client, access_token, temp_loans, temp_loans_db):
    loan_id = temp_loans["loan_ids"][0]

    response = client.get(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    item = response.json()

    assert item["loan_id"] == loan_id
    assert item["book_id"] == temp_loans_db["book_ids"][1]
    assert item["user_id"] == temp_loans["user_id"]


@pytest.mark.parametrize(
    "loan_id, expected_status_code",
    (
        (0, 422),
        (-1, 422),
        (-1000, 422),
        ("abc", 422),
        (100, 404),
    )
)
def test_get_loan_by_id_not_found(
    client, access_token, loan_id, expected_status_code
):
    response = client.get(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == expected_status_code


def test_create_loan(client, access_token, temp_loans, temp_loans_db):
    new_loan = {
        "book_id": temp_loans_db["book_ids"][1],
        "loan_date": date.today().isoformat()
    }

    response = client.post(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_loan
    )

    assert response.status_code == 200
    assert response.json()["book_id"] == new_loan["book_id"]
    assert response.json()["user_id"] == temp_loans["user_id"]
    assert response.json()["loan_id"] is not None


def test_create_loan_fails_with_invalid_data(client, access_token):
    invalid_loan = {
        "title": "Invalid loan",
        "author": "Bitar",
        "genre": "Sci-Fi"
    }

    response = client.post(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        json=invalid_loan
    )

    assert response.status_code == 422


def test_delete_loan(client, access_token, temp_loans):
    loan_id = temp_loans["loan_ids"][0]

    response = client.delete(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    response = client.get(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404


def test_delete_loan_not_found(client, access_token):
    response = client.delete(
        "/loans/200",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert response.json()["details"] == "Loan with id 200 doesn't exist"


def test_update_loan(client, access_token, temp_loans, temp_loans_db):
    loan_id = temp_loans["loan_ids"][0]

    updated_loan = {
        "book_id": temp_loans_db["book_ids"][4],
        "loan_date": date.today().isoformat()
    }

    response = client.put(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_loan
    )

    assert response.status_code == 200

    response = client.get(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200

    item = response.json()

    assert item["book_id"] == updated_loan["book_id"]
    assert item["loan_date"] == date.today().isoformat()
    assert item["user_id"] == temp_loans["user_id"]



def test_get_loans_filtered_by_book(
    client, access_token, temp_loans, temp_loans_db
):
    book_id = temp_loans_db["book_ids"][2]

    response = client.get(
        "/loans",
        params={
            "book_id": book_id,
            "min_date": "2026-01-20",
            "max_date": "2026-01-20"
        },
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    items = response.json()["items"]

    assert len(items) == 1
    assert items[0]["book_id"] == book_id
    assert items[0]["loan_date"] == "2026-01-20"


def test_get_loans_pagination_with_parameters(client, access_token, temp_loans):
    response = client.get(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"}, 
        params={
            "offset": 1, 
            "limit": 1,
            "min_date":"2026-01-20",
            "max_date":"2026-01-20",
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 2
    assert len(data["items"]) == 1


def test_create_loan_with_non_existing_book(client, access_token):
    new_loan = {
        "book_id": 1354,
        "loan_date": date.today().isoformat()
    }

    response = client.post(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        json=new_loan
    )

    assert response.status_code == 404


def test_update_loan_with_non_existing_book(
    client, access_token, temp_loans
):
    loan_id = temp_loans["loan_ids"][0]

    updated_loan = {
        "book_id": 1355,
        "loan_date": date.today().isoformat()
    }

    response = client.put(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_loan
    )

    assert response.status_code == 404


def test_update_loan_not_found(client, access_token, temp_loans_db):
    updated_loan = {
        "book_id": temp_loans_db["book_ids"][0],
        "loan_date": date.today().isoformat()
    }

    response = client.put(
        "/loans/100",
        headers={"Authorization": f"Bearer {access_token}"},
        json=updated_loan
    )

    assert response.status_code == 404


def test_user_cannot_access_another_users_loan(
    client, access_token, temp_loans
):
    second_user = {
        "username": "seconduser",
        "full_name": "Second User",
        "email": "second@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=second_user
    )

    assert register_response.status_code == 200

    second_token = register_response.json()["access_token"]
    loan_id = temp_loans["loan_ids"][0]

    response = client.get(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {second_token}"}
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_loan(
    client, temp_loans, register_user
):
    second_user = {
        "username": "seconduser",
        "full_name": "Second User",
        "email": "second@example.com",
        "password": "password123"
    }

    register_response = client.post(
        "/auth/register",
        json=second_user
    )

    assert register_response.status_code == 200

    second_token = register_response.json()["access_token"]
    loan_id = temp_loans["loan_ids"][0]

    response = client.delete(
        f"/loans/{loan_id}",
        headers={"Authorization": f"Bearer {second_token}"}
    )

    assert response.status_code == 404

def test_get_loans_with_invalid_parameters(
    client, temp_loans, register_user
):

    response = client.get(
        "/loans",
        headers={"Authorization": f"Bearer {access_token}"},
        params={
            "min_date": "2026-01-20",
            "max_date": "2026-01-10"
        },
    )

    assert response.status_code == 401