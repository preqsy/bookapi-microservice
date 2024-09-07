import pytest
from httpx import AsyncClient
from fastapi import status

from tests.sample_datas.book_samples import (
    sample_book_create,
    sample_borrowed_book_create,
    sample_search_category,
    sample_search_nonexistent_category,
    sample_search_nonexistent_publisher,
    sample_search_publisher,
)


async def add_book(client: AsyncClient, book_details: dict = sample_book_create()):
    response = await client.post("/books/", json=book_details)
    return response


async def borrow_book(
    client: AsyncClient, borrow_details: dict = sample_borrowed_book_create()
):
    response = await client.post("/books/borrow", json=borrow_details)
    return response


@pytest.mark.asyncio
async def test_add_book_success(client: AsyncClient):
    response = await add_book(client)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_add_book_with_missing_data(client: AsyncClient):
    book_data = sample_book_create()
    del book_data["title"]  # Simulate missing title field

    response = await client.post("/books/", json=book_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_borrow_book_success(client: AsyncClient):
    # Add a book first
    await add_book(client)

    # Borrow the book
    response = await borrow_book(client)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_borrow_book_already_borrowed(client: AsyncClient):
    await add_book(client)

    await borrow_book(client)

    response = await borrow_book(client)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_list_books(client: AsyncClient):
    await add_book(client)
    response = await client.get("/books/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_list_books_no_books(client: AsyncClient):
    response = await client.get("/books/")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_get_book_by_id(client: AsyncClient):
    response = await add_book(client)
    book_id = response.json()["id"]

    response = await client.get(f"/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_filter_books_by_category(client: AsyncClient):
    await add_book(client)

    response = await client.post("/books/category", json=sample_search_category())
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_filter_books_by_nonexistent_category(client: AsyncClient):
    await add_book(client)

    response = await client.post(
        "/books/category", json=sample_search_nonexistent_category()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_filter_books_by_publisher(client: AsyncClient):
    await add_book(client)

    response = await client.post("/books/publisher", json=sample_search_publisher())
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_filter_books_by_nonexistent_publisher(client: AsyncClient):
    await add_book(client)

    response = await client.post(
        "/books/publisher", json=sample_search_nonexistent_publisher()
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_remove_book(client: AsyncClient):
    response = await add_book(client)
    book_id = response.json()["id"]

    response = await client.delete(f"/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_remove_book_invalid_id(client: AsyncClient):
    response = await add_book(client)

    response = await client.delete(f"/books/{109}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
