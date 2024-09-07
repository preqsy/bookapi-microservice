from typing import Optional
import requests
from fastapi import status, APIRouter
from schemas.books import (
    BorrowedBookCreate,
    SearchCategories,
    SearchPublisher,
)
from core.errors import InvalidRequest


router = APIRouter(prefix="/books")

ADMIN_API_URL = "http://admin_web:8000/books"


@router.get("/get-all")
def get_all_books():
    response = requests.get(url=f"{ADMIN_API_URL}/")
    if response.status_code == 200:
        return response.json()
    raise InvalidRequest


@router.get("/books/{id}")
def single_book(id: int):
    response = requests.get(url=f"{ADMIN_API_URL}/{id}")
    if response.status_code == 200:
        return response.json()
    raise InvalidRequest


@router.post("/category")
def get_books_by_category(book_cat: SearchCategories, limit: Optional[int] = 10):
    response = requests.post(
        url=f"{ADMIN_API_URL}/category",
        json=book_cat.model_dump(),
        params={"limit": limit},
    )
    if response.status_code == status.HTTP_200_OK:
        return response.json()
    raise InvalidRequest


@router.post("/publisher")
def get_books_by_publisher(book_publisher: SearchPublisher, limit: Optional[int] = 10):
    response = requests.post(
        url=f"{ADMIN_API_URL}/publisher",
        json=book_publisher.model_dump(),
        params={"limit": limit},
    )
    if response.status_code == 200:
        return response.json()
    raise InvalidRequest


@router.post("/borrow")
def borrow_book(data: BorrowedBookCreate):
    response = requests.post(url=f"{ADMIN_API_URL}/borrow", json=data.model_dump())
    if response.status_code == 200:
        return response.json()
    raise InvalidRequest
