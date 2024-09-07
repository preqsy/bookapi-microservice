from typing import List, Optional
from fastapi import Depends, HTTPException, status, APIRouter
from schemas.books import (
    BookOut,
    SearchCategories,
)
from crud import CRUDBook, get_crud_book

router = APIRouter(prefix="/books")


# main.py
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, status
from schemas import BookOut, SearchCategories
from crud import CRUDBook

app = FastAPI()


@app.get("/books/", response_model=List[BookOut])
def get_all_books(
    crud_book: CRUDBook = Depends(get_crud_book),
    limit: Optional[int] = 10,
    search: Optional[str] = "",
):
    return crud_book.get_books(search=search, limit=limit)


@app.get("/books/{id}", response_model=BookOut)
def single_book(
    id: int,
    crud_book: CRUDBook = Depends(get_crud_book),
):
    book = crud_book.get_book_by_id(book_id=id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
        )
    return book


@app.post("/books/categories", response_model=List[BookOut])
def get_books_by_categories(
    book_cat: SearchCategories,
    crud_book: CRUDBook = Depends(get_crud_book),
    limit: Optional[int] = 10,
):
    return crud_book.get_books_by_category(category=book_cat.categories, limit=limit)


@app.post("/books/{id}/borrow")
def borrow_book(
    id: int,
    days: int,
    crud_book: CRUDBook = Depends(get_crud_book),
):
    book = crud_book.borrow_book(book_id=id, days=days)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not available or not found",
        )
    return book
