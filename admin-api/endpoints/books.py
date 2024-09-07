from datetime import date, timedelta
from typing import List, Optional
from fastapi import Depends, status, APIRouter
from schemas.books import (
    BookCreate,
    BookOut,
    SearchCategories,
    SearchPublisher,
    BorrowedBookCreate,
    BorrowedBookReturn,
    Borrowed,
)

from crud import CRUDBook, get_crud_book, get_crud_borrowed_book, CRUDBorrowBook
from core.errors import MissingResources, InvalidRequest

router = APIRouter(prefix="/books")


@router.post("/", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def add_book(
    book: BookCreate,
    crud_book: CRUDBook = Depends(get_crud_book),
):
    book.author = str(book.author).title()
    return crud_book.create_book(data=book.model_dump())


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_book(
    id: int,
    crud_book: CRUDBook = Depends(get_crud_book),
):
    crud_book.get_book_by_id_or_raise_exception(book_id=id)
    crud_book.delete_book(book_id=id)
    return


@router.get("/", response_model=List[BookOut])
def list_books(
    crud_book: CRUDBook = Depends(get_crud_book),
    limit: Optional[int] = 10,
    search: Optional[str] = "",
):
    books = crud_book.get_books(search=search, limit=limit)
    if not books:
        raise MissingResources("No books right now")
    return books


@router.get("/get-borrowed-books", response_model=list[BorrowedBookReturn])
def borrow_book(
    crud_book: CRUDBook = Depends(get_crud_book),
):

    borrowed_books = crud_book.get_borrowed_books()
    if not borrowed_books:
        raise MissingResources("No borrowed books currently")

    return borrowed_books


@router.get("/{id}", response_model=BookOut)
def get_book(
    id: int,
    crud_book: CRUDBook = Depends(get_crud_book),
):
    book = crud_book.get_book_by_id_or_raise_exception(book_id=id)
    return book


@router.post("/category", response_model=List[BookOut])
def filter_books_by_category(
    book_cat: SearchCategories,
    crud_book: CRUDBook = Depends(get_crud_book),
    limit: Optional[int] = 10,
):
    books = crud_book.get_books_by_category(category=book_cat.category, limit=limit)
    if not books:
        raise MissingResources(f"No book in the category: {book_cat.category}")
    return books


@router.post("/publisher", response_model=List[BookOut])
def filter_books_by_category(
    book_publisher: SearchPublisher,
    crud_book: CRUDBook = Depends(get_crud_book),
    limit: Optional[int] = 10,
):
    book_publisher.publisher = str(book_publisher.publisher).title()
    books = crud_book.get_books_by_publisher(
        publisher=book_publisher.publisher, limit=limit
    )
    if not books:
        raise MissingResources(
            f"No book with the publisher: {book_publisher.publisher}"
        )
    return books


@router.post("/borrow", response_model=Borrowed)
def borrow_book(
    data_obj: BorrowedBookCreate,
    crud_book: CRUDBook = Depends(get_crud_book),
    crud_borrowed_book: CRUDBorrowBook = Depends(get_crud_borrowed_book),
):

    book = crud_book.get_book_by_id_or_raise_exception(book_id=data_obj.book_id)

    if not book.is_available:
        raise InvalidRequest("Book borrowed by another user")
    due_date = date.today() + timedelta(days=data_obj.days_to_borrow)
    data_obj.due_date = due_date

    book = crud_borrowed_book.borrow_book(data_dict=data_obj.model_dump())
    crud_book.update_book(
        book_id=data_obj.book_id,
        data={"is_available": False, "available_date": due_date},
    )
    return Borrowed()
